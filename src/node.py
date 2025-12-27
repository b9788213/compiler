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
    name: str
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
    name: str
    args: list

@dataclass()
class Ret:
    value: Any

@dataclass()
class Var:
    name: str
    offset: int

@dataclass()
class Program:
    funcs: list[Func]
    statics: list[Id]

@dataclass()
class Func:
    name: str
    args: list[str]
    body: list
    vars: list[Var] = field(default_factory=list[Var])