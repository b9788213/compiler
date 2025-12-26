import re
from typing import NamedTuple

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

    __str__ = lambda self: f"{self.type} {self.value}"

token_specification = (
    ('STRING',      r'".*?"'),             # stringler

    ('FN',          r'\bfn\b'),            # Fonksiyon tanımı
    ('RET',         r'\breturn\b'),        # Geri dönüş değeri
    ('IMPORT',      r'\bimport\b'),        # Kütüphane ekleme
    ('STATIC',      r'\bglobal\b'),         # static değişken

    ('EQ',          r'=='),                # Eşittir
    ('NE',          r'!='),                # Eşit Değildir
    ('LE',          r'<='),                # Küçük Eşittir
    ('GE',          r'=>'),                # Büyük Eşittir
    ('LT',          r'<'),                 # Küçüktür
    ('GT',          r'>'),                 # Büyüktür

    ('COLON',       r':'),
    ('COMMA',       r','),
    ('LPAR',        r'\('),                # Kaçış karakteri eklendi
    ('RPAR',        r'\)'),                # Kaçış karakteri eklendi

    ('NUMBER',      r'\d+(\.\d+)?'),       # .5 gibi hatalı sayıları önlemek için + kullanıldı
    ('ASSIGN',      r'='),
    ('ID',          r'[A-Za-z_]\w*'),      # Değişken isimleri
    ('OP',          r'[+\-*/]'),           # Operatörler

    ('NEWLINE',     r'\n'),                # Satır sonu
    ('SKIP',        r'[ \t]+'),            # Sadece satır içi boşluklar
    ('MISMATCH',    r'.'),                 # Beklenmeyen karakterler
)

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)


def lex(code):
    line_num = 1
    line_start = 0
    indent_stack = [0]
    at_line_start = True

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        # Sütun hesabı her zaman o anki eşleşmenin (mo) başladığı yere göre yapılmalı
        column = mo.start() - line_start + 1

        if kind == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            at_line_start = True
            continue

        if at_line_start:
            # Satırın tamamen boş olup olmadığını (veya sadece yorum olduğunu) kontrol et
            remaining = code[mo.start():].split('\n')[0]
            if not remaining.strip(): continue


            # Girinti miktarını hesapla
            current_indent = len(value) if kind == 'SKIP' else 0

            # INDENT / DEDENT üretimi
            if current_indent > indent_stack[-1]:
                indent_stack.append(current_indent)
                yield Token('INDENT', " ", line_num, column)

            while current_indent < indent_stack[-1]:
                indent_stack.pop()
                yield Token('DEDENT', '', line_num, column)

            at_line_start = False
            # Eğer bu bir SKIP tokenı ise (boşluk), onu yield etmiyoruz ama sütun bilgisini tüketmiş olduk.
            if kind == 'SKIP': continue

            # Normal tokenları işle
        if kind == "SKIP" or kind == "NEWLINE": continue

        if kind == "MISMATCH": raise RuntimeError(f'{value!r} beklenmeyen karakter. Satır: {line_num}, Sütun: {column}')

        yield Token(kind, value, line_num, column)

    # Dosya sonu temizliği
    while len(indent_stack) > 1:
        indent_stack.pop()
        yield Token('DEDENT', '', line_num, 1)