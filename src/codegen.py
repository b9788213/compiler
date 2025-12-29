from node import *

regs = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")

class CodeGen:
    def __init__(self, p: Program):
        self.p = p
        self.asm: list[str] = []
        self.data: dict[str, str] = {} #değişken ismi, label
        self.currentf: Func =  None
        self.strings: dict[str, str] = {} # label, string
        self.isaligned: bool = True
        self.rand = 0

    def emit(self, s: str):
        self.asm.append(s)

    def emitstack(self, s):
        self.emit(s)
        self.isaligned = not self.isaligned

    def getlabel(self):
        self.rand += 1
        return f"label_{self.rand}"

    def gen(self):
        for s in self.p.statics: #staticleri kaydet
            self.data[s.name] = self.getlabel()

        self.emit("bits 64")
        self.emit("default rel")
        self.emit("section .text")
        self.emit("global main")

        for f in self.p.funcs:
            self.gen_func(f)

        self.emit("section .data")
        for l in self.data.values():
            self.emit(f"{l}: dq 0")

        self.emit("section .rodata")
        for l, s in self.strings.items():
            bytes_val = s.encode('utf-8')
            ascii_val = ", ".join(str(b) for b in bytes_val)
            self.emit(f"{l}: db {ascii_val}, 0")

        self.emit("section .note.GNU-stack noalloc noexec nowrite progbits")
        return "\n".join(self.asm)

    def gen_func(self, f: Func):
        f.vars.update(dict.fromkeys(f.args)) #parametreleri değişken yap
        self.currentf = f
        self.isaligned = True

        self.emit(f"{f.name}:")
        self.emit("push rbp") # rbp + return adress zaten 16 byte
        self.emit("mov rbp, rsp")
        self.emit(f"sub rsp, {stack(f)}")

        for i, var in enumerate(f.args): #parametreleri stacke koy
            self.emit(f"mov [rbp {f.vars[var]:+d}], {regs[i]}")

        self.gen_body(f.body)

        self.emit("xor rax, rax") # return yoksa 0 döndür
        self.emit(".exit:")
        if f.name == "main":
            self.emit("mov rdi, rax")
            self.emit("mov rax, 60")
            self.emit("syscall")
        else:
            self.emit("leave")
            self.emit("ret")

    def gen_body(self, b: Body):
        for stmt in b.code:

            if isinstance(stmt, Asm):
                self.emit(stmt.value)

            elif isinstance(stmt, Assign):
                self.gen_expr(stmt.value)

                if stmt.name in self.data.keys():
                    self.emit(f"mov [{self.data[stmt.name]}], rax")
                else:
                    self.emit(f"mov [rbp {self.currentf.vars[stmt.name]:+d}], rax ")

            elif isinstance(stmt, Call):
                self.call(stmt)

            elif isinstance(stmt, ConditionelStruct):
                labels = []
                for _ in stmt.ifs: labels.append(self.getlabel()) # if labels
                labels.append(self.getlabel()) # else label
                endlab = self.getlabel()

                for i, if_ in enumerate(stmt.ifs):
                    self.emit(f".{labels[i]}:")
                    self.gen_expr(if_.cond) # değer rax'ta
                    self.emit("test rax, rax")
                    self.emit(f"jz .{labels[i+1]}")
                    self.gen_body(if_.body)
                    self.emit(f"jmp .{endlab}")

                self.emit(f".{labels[-1]}:")
                if stmt.elsebody: self.gen_body(stmt.elsebody)
                self.emit(f".{endlab}:")

            elif isinstance(stmt, While):
                startlab = self.getlabel()
                endlab = self.getlabel()

                self.emit(f".{startlab}:")
                self.gen_expr(stmt.cond)
                self.emit(f"jz .{endlab}")
                self.gen_body(stmt.body)
                self.emit(f"jmp .{startlab}")
                self.emit(f".{endlab}:")

            elif isinstance(stmt, Ret):
                self.gen_expr(stmt.value)
                self.emit("jmp .exit")
                break # gereksiz kısımları üretme

    def gen_expr(self, expr):

        if isinstance(expr, Call):
            self.call(expr)

        elif isinstance(expr, Id):
            if expr.name in self.data.keys():
                self.emit(f"mov rax, [{self.data[expr.name]}]")
            else:
                self.emit(f"mov rax, [rbp {self.currentf.vars[expr.name]:+d}]")

        elif isinstance(expr, Int):
            self.emit(f"mov rax, {expr.value}")

        elif isinstance(expr, Float):
            raise NotImplementedError("Not implemented float")

        elif isinstance(expr, String):
            label = self.getlabel()
            self.strings[label] = expr.value
            self.emit(f"mov rax, {label}")

        elif isinstance(expr, Neg):
            self.gen_expr(expr.value)
            self.emit("neg rax")

        elif isinstance(expr, BinOp):
            self.ready(expr)

            if expr.op == "PLUS":
                self.emit("add rax, rbx")
            elif expr.op == "MINUS":
                self.emit("sub rax, rbx")
            elif expr.op == "MUL":
                self.emit("imul rax, rbx")
            elif expr.op in ("DIV", "MOD"):
                self.emit("cqo")
                self.emit("idiv rbx")
                if expr.op == "MOD": self.emit("mov rax, rdx")

        elif isinstance(expr, Comp):
            self.ready(expr)
            self.emit("cmp rax, rbx")

            if expr.op == "EQEQ": self.emit("sete al")
            if expr.op == "NEQ": self.emit("setne al")
            if expr.op == "LEQ": self.emit("setle al")
            if expr.op == "GEQ": self.emit("setge al")
            if expr.op == "LT": self.emit("setl al")
            if expr.op == "GT": self.emit("setg al")

            self.emit("movzx rax, al")

    def ready(self, expr):
        self.gen_expr(expr.right)
        self.emitstack("push rax")
        self.gen_expr(expr.left)
        self.emitstack("pop rbx")

    def call(self, c: Call):
        needed = regs[:len(c.args)]
        rev = needed[::-1]

        for arg in c.args:
            self.gen_expr(arg)
            self.emitstack("push rax")

        for i in range(len(c.args)):
            self.emitstack(f"pop {rev[i]}")

        if not self.isaligned:
            self.emitstack("push 0")  # şimdi hizalı
            self.emit(f"call {c.name}")  # 8 byte return adress
            self.emitstack("add rsp, 8")
        else:
            self.emit(f"call {c.name}")

def stack(f: Func) -> int:
    offset = 0
    size = len(f.vars) * 8

    for var in f.vars:
        offset -= 8
        f.vars[var] = offset

    return (size + 15) & ~15
