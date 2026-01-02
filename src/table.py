from dataclasses import dataclass, field

@dataclass()
class Var:
    name: str
    address: str = ""

@dataclass()
class Func:
    name: str
    vars: list[Var] =  field(default_factory=list)

    def addVar(self, name: str):
        self.vars.append(Var(name))

    def setVar(self, name: str, val: str):
        for n in self.vars:
            if n.name == name:
                n.address = val
        raise RuntimeError(f"Cannot find local variable: {name}")


    def getVar(self, name: str):
        for n in self.vars:
            if n.name == name:
                return n.address
        raise RuntimeError(f"Cannot find local variable: {name}")

class Table:
    funcs: list[Func] = []
    scope: Func

    def enterScope(self, name: str):
        for f in self.funcs:
            if f.name == name:
                self.scope = f

        raise RuntimeError(f"cannot find function: {name}")
