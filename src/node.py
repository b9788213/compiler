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
class Program:
    funcs: list[Func]  = field(default_factory=list)
    statics: list[Id]  = field(default_factory=list)

@dataclass()
class Func:
    name: str
    args: list[str]  = field(default_factory=list)
    body: list  = field(default_factory=list)
    vars: dict[str, int] = field(default_factory=dict)