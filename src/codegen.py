from node import *

class Reg(tuple):
    def __getitem__(self, i):
        try: super().__getitem__(i)
        except Exception: raise NotImplementedError("cant send More Than 6 parameters")

regs = Reg(("rdi", "rsi", "rdx", "rcx", "r8", "r9"))

class CodeGen:
    def __init__(self, p: Program):
        self.p = p
        self.asm: list[str] = []
        self.data: dict[str, str] = {}
        self.currentf: Func =  None
        self.rand = 0

    def emit(self, s: str):
        self.asm.append(s)

    def getlabel(self):
        self.rand += 1
        return f"label_{self.rand}"

    def gen(self):
        for s in self.p.statics: #staticleri kaydet
            self.data[s.name] = self.getlabel()

        self.emit("section .text")
        self.emit("global _start")
        self.emit("_start:")
        self.emit("call main")
        self.emit("mov rdi, rax")
        self.emit("mov rax, 60")
        self.emit("syscall")

        for f in self.p.funcs:
            self.gen_func(f)

        return "\n".join(self.asm)

    def gen_func(self, f: Func):
        f.vars.update(dict.fromkeys(f.args, 0)) #parametreleri değişken yap
        self.currentf = f

        self.emit(f"{f.name}:")
        self.emit("push rbp")
        self.emit("mov rbp, rsp")
        self.emit(f"sub rsp, {stack(f)}")

        for i, var in enumerate(f.args): #parametreleri kaydet
            self.emit(f"mov [rbp {f.vars[var]:+d}], {regs[i]}")

        self.gen_body(f.body)

        self.emit(".exit:")
        self.emit("leave")
        self.emit("ret")

    def gen_body(self, b: Body):
        for ast in b.code:

            if isinstance(ast, Assign):
                continue

            if isinstance(ast, Call):
                continue

            if isinstance(ast, Ret):
                self.gen_expr(ast.value)
                self.emit("jmp .exit")
                break # gereksiz kısımları üretmez

    def gen_expr(self, expr):

        if isinstance(expr, Call):
            pass

        elif isinstance(expr, Id):
            if expr.name in self.data.keys():
                self.emit(f"mov rax, [{self.data[expr.name]}]")
            else:
                try: self.emit(f"mov rax, [{self.currentf.vars[expr.name]}]")
                except: raise RuntimeError(f"Cant find local variable {expr.name}")

        elif isinstance(expr, Int):
            self.emit(f"mov rax, {expr.value}")

        elif isinstance(expr, Float):
            pass

        elif isinstance(expr, String):
            pass

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
            elif expr.op == "DIV":
                self.emit("cqo")
                self.emit("idiv rbx")

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
        self.emit("push rax")
        self.gen_expr(expr.left)
        self.emit("pop rbx")

def stack(f: Func) -> int:
    offset = 0
    size = len(f.vars) * 8
    remainder = size % 16

    for var in f.vars:
        offset -= 8
        f.vars[var] = offset

    return remainder + size