from dataclasses import dataclass

@dataclass()
class Func:
    name: str
    vars: list[Var] = []

    def getVar(self, name: str):
        for n in self.vars:
            if n.name == name:
                return n.address
        raise RunTimeError(f"Cannot find local variable: {name}")

@dataclass()
class Var:
    name: str
    address: str
