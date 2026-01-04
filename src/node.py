from dataclasses import dataclass, field
from typing import Any


@dataclass
class Id:
    id: str


@dataclass
class Int:
    value: int


@dataclass
class Float:
    value: float


@dataclass
class String:
    value: str


@dataclass
class Assign:
    id: Id
    value: Any


@dataclass
class BinOp:
    op: str
    left: Any
    right: Any


@dataclass
class Neg:
    value: Any


@dataclass
class Comp:
    op: str
    left: Any
    right: Any


@dataclass
class Call:
    id: Id
    args: list


@dataclass
class Ret:
    value: Any


@dataclass
class Body:
    code: list = field(default_factory=list)


@dataclass
class Func:
    id: Id
    args: list[str] = field(default_factory=list)
    body: Body = field(default_factory=Body)


@dataclass
class Asm:
    value: str


@dataclass
class If:
    cond: Comp
    body: Body = field(default_factory=Body)


@dataclass
class CondStruct:
    ifs: list[If]
    elsebody: Body | None


@dataclass
class While:
    cond: Comp
    body: Body


@dataclass
class Program:
    funcs: list[Func] = field(default_factory=list)
