import re
from typing import NamedTuple, Iterator


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return f"{self.type}, {self.value}, at line {self.line}, column {self.column}"


token_specification = (
    ('STR', r'"(?:\\.|[^"\\])*"'),

    ('ASM', r'\basm\b'),
    ('FN', r'\bfn\b'),
    ('RET', r'\breturn\b'),
    ('IMPORT', r'\bimport\b'),
    ('STATIC', r'\bglobal\b'),

    ('ELIF', r'\belif\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),

    ('EQEQ', r'=='),
    ('NEQ', r'!='),
    ('LEQ', r'<='),
    ('GEQ', r'=>'),
    ('LT', r'<'),
    ('GT', r'>'),

    ('COLON', r':'),
    ('COMMA', r','),
    ('LPAR', r'\('),
    ('RPAR', r'\)'),

    ('FLOAT', r'\d+\.\d+'),
    ('INT', r'\d+'),
    ('EQ', r'='),
    ('ID', r'[A-Za-z_]\w*'),

    ('PLUS',        r'\+'),
    ('MINUS',       r'-'),
    ('MUL',         r'\*'),
    ('DIV',         r'/'),
    ('MOD',         r'%'),

    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
)

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)


def lex(code: str) -> Iterator[Token]:
    line_num = 1
    line_start = 0
    indent_stack = [0]
    at_line_start = True

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            at_line_start = True
            continue

        if at_line_start:
            # Sadece boşluklardan oluşan veya boş satırları atlamak için ileriye bak
            next_newline = code.find('\n', mo.start())
            line_end = next_newline if next_newline != -1 else len(code)
            line_content = code[mo.start():line_end]

            if not line_content.strip():
                # Eğer satır sadece boşluk veya boşsa, bu tokenı geç ve satır başına devam et
                continue

            # Girinti miktarını hesapla (sadece SKIP ise değeri al, değilse 0)
            indent_level = len(value) if kind == 'SKIP' else 0

            if indent_level > indent_stack[-1]:
                indent_stack.append(indent_level)
                yield Token('INDENT', str(indent_level), line_num, column)

            while indent_level < indent_stack[-1]:
                indent_stack.pop()
                yield Token('DEDENT', '', line_num, column)

            at_line_start = False
            if kind == 'SKIP': continue

        if kind == 'MISMATCH':
            raise RuntimeError(f'Hata: {value!r} geçersiz karakter (Satır {line_num}, Sütun {column})')

        if kind == 'SKIP': # Normal boşlukları atla
            continue

        if kind == 'STR':
            value = value[1:-1].encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8') # tırnakları at, escapeleri çöz

        yield Token(kind, value, line_num, column)

    # Dosya sonunda kalan girintileri kapat
    while len(indent_stack) > 1:
        indent_stack.pop()
        yield Token('DEDENT', '', line_num, 1)

    yield Token('EOF', '', line_num, 1)