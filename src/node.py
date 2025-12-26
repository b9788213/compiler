from typing import NamedTuple, Any

class Id(NamedTuple):
    name: str

class Int(NamedTuple):
    value: int

class Float(NamedTuple):
    value: float

class String(NamedTuple):
    value: str

class Assign(NamedTuple):
    name: str
    value: Any

class BinOp(NamedTuple):
    op: str
    left: Any
    right: Any

class Neg(NamedTuple):
    value: Any

class Comp(NamedTuple):
    op: str
    left: Any
    right: Any

class Call(NamedTuple):
    name: str
    args: list

class Program(NamedTuple):
    funcs: list[Func]
    statics: list

class Func(NamedTuple):
    name: str
    args: list
    body: list