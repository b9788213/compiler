import node as n
import table as t
import constants as c

regs = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")


class CodeGen:
    def __init__(self, p: n.Program):
        self.p = p
        self.asm: list[str] = []
        self.strings: dict[str, str] = {}  # label, string
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
        for s in t.statics:  # staticleri kaydet
            t.setStatic(s.name, self.getlabel())

        self.emit("bits 64")
        self.emit("default rel")
        self.emit("section .text")
        self.emit("global main")

        for f in self.p.funcs:
            self.gen_func(f)

        self.emit("section .data")
        for static in t.statics:
            self.emit(f"{static.address}: dq 0")

        self.emit("section .rodata")
        for lab, s in self.strings.items():
            bytes_val = s.encode("utf-8")
            ascii_val = ", ".join(str(b) for b in bytes_val)
            self.emit(f"{lab}: db {ascii_val}, 0")

        self.emit("section .note.GNU-stack noalloc noexec nowrite progbits")
        return "\n".join(self.asm)

    def gen_func(self, f: n.Func):
        t.enterScope(f.name.name)
        self.isaligned = True

        self.emit(f"{f.name.name}:")
        self.emit("push rbp")  # rbp + return adress zaten 16 byte
        self.emit("mov rbp, rsp")
        self.emit(f"sub rsp, {self.stack()}")

        for i, var in enumerate(f.args):  # parametreleri stacke koy
            self.emit(f"mov {t.getVar(var)}, {regs[i]}")

        self.gen_body(f.body)

        self.emit("xor rax, rax")  # return yoksa 0 döndür
        self.emit(".exit:")
        if f.name == "main":
            self.emit("mov rdi, rax")
            self.emit("mov rax, 60")
            self.emit("syscall")
        else:
            self.emit("leave")
            self.emit("ret")

    def gen_body(self, b: n.Body):
        for stmt in b.code:

            if isinstance(stmt, n.Asm):
                self.emit(stmt.value)

            elif isinstance(stmt, n.Assign):
                self.gen_expr(stmt.value)

                if stmt.name.name in (static.name for static in t.statics):
                    self.emit(f"mov [{t.getStatic(stmt.name.name)}], rax")
                else:
                    self.emit(f"mov {t.getVar(stmt.name.name)}, rax ")

            elif isinstance(stmt, n.Call):
                self.call(stmt)

            elif isinstance(stmt, n.CondStruct):
                labels = []
                for _ in stmt.ifs:
                    labels.append(self.getlabel())  # if labels
                labels.append(self.getlabel())  # else label
                endlab = self.getlabel()

                for i, if_ in enumerate(stmt.ifs):
                    self.emit(f".{labels[i]}:")
                    self.gen_expr(if_.cond)  # değer rax'ta
                    self.emit("test rax, rax")
                    self.emit(f"jz .{labels[i+1]}")
                    self.gen_body(if_.body)
                    self.emit(f"jmp .{endlab}")

                self.emit(f".{labels[-1]}:")
                if stmt.elsebody:
                    self.gen_body(stmt.elsebody)
                self.emit(f".{endlab}:")

            elif isinstance(stmt, n.While):
                startlab = self.getlabel()
                endlab = self.getlabel()

                self.emit(f".{startlab}:")
                self.gen_expr(stmt.cond)
                self.emit("test rax, rax")
                self.emit(f"jz .{endlab}")
                self.gen_body(stmt.body)
                self.emit(f"jmp .{startlab}")
                self.emit(f".{endlab}:")

            elif isinstance(stmt, n.Ret):
                self.gen_expr(stmt.value)
                self.emit("jmp .exit")
                break  # gereksiz kısımları üretme

    def gen_expr(self, expr):
        match expr:
            case n.Call():
                self.call(expr)

            case n.Id():
                if expr.name in (static.name for static in t.statics):
                    self.emit(f"mov rax, [{t.getStatic(expr.name)}]")
                else:
                    self.emit(f"mov rax, {t.getVar(expr.name)}")

            case n.Int():
                self.emit(f"mov rax, {expr.value}")

            case n.Float():
                raise NotImplementedError("Not implemented float")

            case n.String():
                label = self.getlabel()
                self.strings[label] = expr.value
                self.emit(f"lea rax, {label}")

            case n.Neg():
                self.gen_expr(expr.value)
                self.emit("neg rax")

            case n.BinOp():
                self.ready(expr)

                match expr.op:
                    case  c.PLUS:
                        self.emit("add rax, rbx")
                    case  c.MINUS:
                        self.emit("sub rax, rbx")
                    case  c.MUL:
                        self.emit("imul rax, rbx")
                    case c.DIV:
                        self.emit("cqo")
                        self.emit("idiv rbx")
                    case c.MOD:
                        self.emit("cqo")
                        self.emit("idiv rbx")
                        self.emit("mov rax, rdx")

            case n.Comp():
                self.ready(expr)
                self.emit("cmp rax, rbx")

                match expr.op:
                    case c.EQEQ: self.emit("sete al")
                    case c.NEQ: self.emit("setne al")
                    case c.LEQ: self.emit("setle al")
                    case c.GEQ: self.emit("setge al")
                    case c.LT: self.emit("setl al")
                    case c.GT: self.emit("setg al")

                self.emit("movzx rax, al")

    def ready(self, expr):
        self.gen_expr(expr.right)
        self.emitstack("push rax")
        self.gen_expr(expr.left)
        self.emitstack("pop rbx")

    def call(self, c: n.Call):
        need = regs[: len(c.args)][::-1]

        for arg in c.args:
            self.gen_expr(arg)
            self.emitstack("push rax")

        for i in range(len(c.args)):
            self.emitstack(f"pop {need[i]}")

        if self.isaligned:
            self.emit(f"call {c.name.name}")
        else:
            self.emitstack("sub rsp, 8")  # şimdi hizalı
            self.emit(f"call {c.name.name}")
            self.emitstack("add rsp, 8")

    @staticmethod
    def stack() -> int:
        offset = 0
        size = len(t.scope.vars) * 8

        for var in t.scope.vars:
            offset -= 8
            t.setVar(var.name, f"[rbp {offset:+d}]")

        return (size + 15) & ~15
