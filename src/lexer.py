import re
from typing import NamedTuple, Iterator
from filemng import save_token
from constants import (
    STR,
    ASM,
    STATIC,
    WHILE,
    ELIF,
    IF,
    ELSE,
    RET,
    LPAR,
    RPAR,
    IMPORT,
    EQEQ,
    NEQ,
    LEQ,
    GEQ,
    LT,
    FN,
    GT,
    DOT,
    COLON,
    COMMA,
    FLOAT,
    ID,
    INT,
    EQ,
    PLUS,
    MINUS,
    MUL,
    DIV,
    NL,
    MOD,
    EOF, INDENT, DEDENT
)


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return (
            f"{self.type}, {self.value}," f" at line {self.line}, column {self.column}"
        )


token_specification = (
    (STR, r'"(?:\\.|[^"\\])*"'),
    (ASM, r"\basm\b"),
    (FN, r"\bfn\b"),
    (RET, r"\breturn\b"),
    (IMPORT, r"\bimport\b"),
    (STATIC, r"\bglobal\b"),
    (WHILE, r"\bwhile\b"),
    (ELIF, r"\belif\b"),
    (IF, r"\bif\b"),
    (ELSE, r"\belse\b"),
    (EQEQ, r"=="),
    (NEQ, r"!="),
    (LEQ, r"<="),
    (GEQ, r"=>"),
    (LT, r"<"),
    (GT, r">"),
    (DOT, r"\."),
    (COLON, r":"),
    (COMMA, r","),
    (LPAR, r"\("),
    (RPAR, r"\)"),
    (FLOAT, r"\d+\.\d+"),
    (INT, r"\d+"),
    (EQ, r"="),
    (ID, r"[A-Za-z_]\w*"),
    (PLUS, r"\+"),
    (MINUS, r"-"),
    (MUL, r"\*"),
    (DIV, r"/"),
    (MOD, r"%"),
    (NL, r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
)

tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)


def lex(code: str) -> list[Token]:
    tokens = list(_lex(code))
    save_token(tokens)
    return tokens


def _lex(code: str) -> Iterator[Token]:
    line_num = 1
    line_start = 0
    indent_stack = [0]
    at_line_start = True

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        val = mo.group()
        column = mo.start() - line_start + 1

        if kind == NL:
            line_start = mo.end()
            line_num += 1
            at_line_start = True
            continue

        if at_line_start:
            # boş satırları atlamak için ileriye bak
            next_newline = code.find("\n", mo.start())
            line_end = next_newline if next_newline != -1 else len(code)
            line_content = code[mo.start() : line_end]

            if not line_content.strip():
                # Eğer satır boşsa, bu tokenı geç ve satır başına devam et
                continue

            # Girinti miktarını hesapla (sadece SKIP ise değeri al, değilse 0)
            indent_level = len(val) if kind == "SKIP" else 0

            if indent_level > indent_stack[-1]:
                indent_stack.append(indent_level)
                yield Token(INDENT, str(indent_level), line_num, column)

            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                yield Token(DEDENT, "", line_num, column)

            at_line_start = False
            if kind == "SKIP":
                continue

        if kind == "MISMATCH":
            raise RuntimeError(
                f"Hata: {val!r} geçersiz karakter "
                f"(Satır {line_num}, Sütun {column})"
            )

        if kind == "SKIP":  # Normal boşlukları atla
            continue

        if kind == STR:  # tırnakları at, escapeleri çöz
            val = (
                val[1:-1]
                .encode("utf-8")
                .decode("unicode_escape")
                .encode("latin-1")
                .decode("utf-8")
            )

        yield Token(kind, val, line_num, column)

    # Dosya sonunda kalan girintileri kapat
    while len(indent_stack) > 1:
        indent_stack.pop()
        yield Token(DEDENT, "", line_num, 1)

    yield Token(EOF, "", line_num, 1)
