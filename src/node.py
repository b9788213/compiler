from typing import NamedTuple

class Program(NamedTuple):
    code: list

class Id(NamedTuple):
    name: str

class Int(NamedTuple):
    value: int

class Float(NamedTuple):
    value: float

class String(NamedTuple):
    value: str
