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

def enterScope(name: str):
    global scope
    for f in funcs:
        if f.name == name:
            scope = f
            return

    raise RuntimeError(f"cannot find function: {name}")

def addVar(name: str):
    scope.vars.append(Var(name))

def addVars(names: list):
    for name in names:
        scope.vars.append(Var(name))

def setVar(name: str, val: str):
    for n in scope.vars:
        if n.name == name:
            n.address = val
            return
    raise RuntimeError(f"Cannot find local variable: {name}")


def getVar(name: str):
    for n in scope.vars:
        if n.name == name:
            return n.address
    raise RuntimeError(f"Cannot find local variable: {name}")
