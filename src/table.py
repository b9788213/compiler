from dataclasses import dataclass, field

@dataclass()
class Var:
    name: str
    address: str = ""

@dataclass()
class Func:
    name: str
    vars: list[Var] =  field(default_factory=list)


funcs: list[Func] = []
scope: Func = None

def addFunc(name: str):
    funcs.append(Func(name))
    print(f"added function: {name}")

def enterScope(name: str):
    global scope
    for f in funcs:
        if f.name == name:
            scope = f
            print(f"entered scope: {name}")
            return
    raise RuntimeError(f"cannot find function: {name}")

def addVar(name: str):
    for v in scope.vars:
        if v.name == name:
            return
    scope.vars.append(Var(name))
    print(f"added var: {name}")

def addVars(names: list):
    for name in names:
        addVar(name)

def setVar(name: str, val: str):
    for n in scope.vars:
        if n.name == name:
            n.address = val
            print(f"settes {name} to {val}")
            return
    raise RuntimeError(f"Cannot find local variable: {name}")


def getVar(name: str):
    for n in scope.vars:
        if n.name == name:

            return n.address
    raise RuntimeError(f"Cannot find local variable: {name}")
