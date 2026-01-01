from dataclasses import dataclass, field

@dataclass()
class Var:
    name: str
    address: str

@dataclass()
class Func:
    name: str
    vars: list[Var] =  field(default_factory=list)

    def getVar(self, name: str):
        for n in self.vars:
            if n.name == name:
                return n.address
        raise RunTimeError(f"Cannot find local variable: {name}")
