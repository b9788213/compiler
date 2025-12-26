from typing import NoReturn

from node import *
from lexer import Token

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index: int = 0
        self.p = Program([], [])

    #-----Helpers-----
    def peek(self, n=0):
        return self.tokens[self.index + n]

    def pop(self):
        t = self.tokens[self.index]
        self.index += 1
        return t

    def expect(self, s):
        t = self.pop()
        if t.type != s: raise SyntaxError(f"Expected {s}, but got {t}. at line {t.line}, column {t.column}")
        return t

    def check(self, s) -> bool:
        return self.peek().type == s

    def match(self, s) -> bool:
        if self.check(s):
            self.pop()
            return True
        return False

    def error(self) -> NoReturn:
        raise SyntaxError(f"Bad Token at line {self.peek().line}, column {self.peek().column}")

    #-----entry-----
    def parse(self):
        while not self.match('EOF'):

            if self.match("IMPORT"):
                self.handle_import(self.expect("ID").value)
                continue

            if self.match("FN"):
                f = self.parse_func()
                self.p.funcs.append(f)
                continue

            self.error()

    def parse_func(self) -> Func:
        f = Func(self.expect("ID").value, [], [])
        self.p.funcs.append(f)

        if self.match("LPAR"):
            #TODO parse args
            self.expect("RPAR")

        self.expect("COLON")
        self.expect("INDENT")

        while not self.match("DEDENT"): f.body.append(self.parse_stmt())

        return f

    def parse_stmt(self):

        if self.check("ID"):
            name = self.pop().value

            #call
            if self.match("LPAR"):
                #TODO parse call
                self.expect("RPAR")

            #assign and declaration
            if self.match("EQ"):
                #TODO parse exp
                pass

            pass

        #Static decleration
        if self.match("STATIC"):
            name = self.expect("ID").value
            self.p.statics.append(name)
            self.expect("EQ")
            #TODO parse exp

        if self.match("RET"):
            #TODO parse exp
            pass

        self.error()

    #-----presedence-----
    def term(self):
        node = self.factor()

        #while

    def factor(self):
        if self.match("MINUS"): return Neg(self.factor())

        if self.check("ID"): return Id(self.pop().value)

        if self.check("INT"): return Int(int(self.pop().value))

        if self.check("FLOAT"): return Float(float(self.pop().value))

        if self.check("STR"): return String(self.pop().value)

        self.error()

    def handle_import(self, name: str):
        pass