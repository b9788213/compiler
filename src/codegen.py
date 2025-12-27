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
        self.emit(f"{f.name}:")
        self.emit("push rbp")
        self.emit("mov rbp, rsp")

        for i in range(len(f.args)):
            self.emit(f"push {regs[i]}")

        self.emit("leave")
        self.emit("ret")