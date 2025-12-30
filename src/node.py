from dataclasses import dataclass, field
from typing import Any

@dataclass()
class Id:
    name: str

@dataclass()
class Int:
    value: int

@dataclass()
class Float:
    value: float

@dataclass()
class String:
    value: str

@dataclass()
class Assign:
    name: Id
    value: Any

@dataclass()
class BinOp:
    op: str
    left: Any
    right: Any

@dataclass()
class Neg:
    value: Any

@dataclass()
class Comp:
    op: str
    left: Any
    right: Any

@dataclass()
class Call:
    name: Id
    args: list

@dataclass()
class Ret:
    value: Any

@dataclass()
class Body:
    code: list = field(default_factory=list)

class Vars(dict[str, int]):
    def __getitem__(self, item):
        try: return super().__getitem__(item)
        except Exception: raise KeyError(f"Cant find local variable {item}")

@dataclass()
class Func:
    name: Id
    args: list[str]  = field(default_factory=list)
    body: Body = field(default_factory=Body)
    vars: Vars= field(default_factory=Vars)

@dataclass()
class Asm:
    value: str

@dataclass()
class If:
    cond: Comp
    body: Body = field(default_factory=Body)

@dataclass()
class ConditionelStruct:
    ifs: list[If]
    elsebody: Body|None = field(default_factory=None.__class__)

@dataclass()
class While:
    cond: Comp
    body: Body


@dataclass()
class Program:
    funcs: list[Func]  = field(default_factory=list)
    statics: list[Id]  = field(default_factory=list)
