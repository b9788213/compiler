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
        self.data = []

    def emit(self, s: str):
        self.asm.append(s)

    def gen(self):
        for s in self.p.statics: self.data.append(s)

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
        pass

def stack(f: Func) -> int:
    offset = 0
    size = len(f.vars) * 8
    remainder = size % 16

    for var in f.vars:
        offset -= 8
        f.vars[var] = offset

    return remainder + size