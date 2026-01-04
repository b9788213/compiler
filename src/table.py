from dataclasses import dataclass, field


@dataclass
class Var:
    name: str
    address: str = ""


@dataclass
class Func:
    name: str
    vars: list[Var] = field(default_factory=list)


funcs: list[Func] = []
scope: Func = None
statics: list[Var] = []


def instatics(name: str) -> bool:
    return name in (static.name for static in statics)


def getStatic(name: str):
    for v in statics:
        if v.name == name:
            return f"[{v.address}]"
    raise RuntimeError(f"cannot find static variable: {name}")


def addStatic(name: str):
    statics.append(Var(name))


def addStatics(names: list):
    addStatics([name for name in names])


def setStatic(name: str, val: str):
    for static in statics:
        if static.name == name:
            static.address = val
            return
    raise RuntimeError(f"cannot find static variable: {name}")


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
    for v in scope.vars:
        if v.name == name:
            return

    for static in statics:
        if static.name == name:
            return

    scope.vars.append(Var(name))


def addVars(names: list):
    for name in names:
        addVar(name)


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
