from dataclasses import dataclass, field
from typing import Any


@dataclass
class Id:
    id: str


@dataclass
class Int:
    val: int


@dataclass
class Float:
    val: float


@dataclass
class String:
    val: str


@dataclass
class Assign:
    id: Id
    val: Any


@dataclass
class BinOp:
    op: str
    left: Any
    right: Any


@dataclass
class Neg:
    val: Any


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
    val: Any


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
    val: str


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
