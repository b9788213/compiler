from enum import Enum, auto


class TokenType(Enum):
    STR = auto()

    ASM = auto()
    FN = auto()
    RET = auto()
    IMP = auto()
    STATIC = auto()

    WHILE = auto()

    IF = auto()
    ELIF = auto()
    ELSE = auto()

    EQEQ = auto()
    NEQ = auto()
    LEQ = auto()
    GEQ = auto()
    LT = auto()
    GT = auto()

    DOT = auto()
    COLON = auto()
    COMMA = auto()
    LPAR = auto()
    RPAR = auto()
    EQ = auto()

    ID = auto()
    FLOAT = auto()
    INT = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    NL = auto()