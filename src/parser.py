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
        raise SyntaxError(f"Bad Token {self.peek()} at line {self.peek().line}, column {self.peek().column}")

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

    #-----func-----
    def parse_func(self) -> Func:
        f = Func(self.expect("ID").value, [], [])

        if self.match("LPAR"):
            #TODO parse args
            self.expect("RPAR")

        self.expect("COLON")
        self.expect("INDENT")

        while not self.match("DEDENT"): f.body.append(self.parse_stmt())

        return f

    #-----stmt-----
    def parse_stmt(self):

        if self.check("ID"):
            name = self.pop().value

            #call
            if self.match("LPAR"):
                #TODO parse call
                self.expect("RPAR")

            #assign and declaration
            if self.match("EQ"):
                return Assign(name, self.compare())

            pass

        #Static decleration
        if self.match("STATIC"):
            name = self.expect("ID").value
            self.p.statics.append(name)
            self.expect("EQ")
            return Assign(name, self.compare())

        if self.match("RET"):
            return Ret(self.compare())

        self.error()

    #-----presedence-----
    def compare(self):
        node = self.expr()

        while self.peek().type in ("EQEQ", "NEQ", "LEQ", "GEQ", "LT", "GT"):
            op = self.pop().type
            node = Comp(op, node, self.expr())
        return node

    def expr(self):
        node = self.term()

        while self.peek().type in ("PLUS", "MINUS"):
            op = self.pop().type
            node =  BinOp(op, node, self.term())
        return node

    def term(self):
        node = self.factor()

        while self.peek().type in ("MUL", "DIV"):
            op = self.pop().type
            node = BinOp(op, node, self.factor())
        return node

    def factor(self):
        if self.match("LPAR"):
            node = self.compare()  # En başa dön!
            self.expect("RPAR")
            return node

        if self.match("MINUS"):
            f = self.factor()

            if isinstance(f, Int): return Int(-1 * f.value)
            if isinstance(f, Float): return Float(-1 * f.value)

            return Neg(f)

        if self.check("ID"): return Id(self.pop().value)

        if self.check("INT"): return Int(int(self.pop().value))

        if self.check("FLOAT"): return Float(float(self.pop().value))

        if self.check("STR"): return String(self.pop().value)

        self.error()

    #-----call-----
    def parse_call(self):
        pass

    def handle_import(self, name: str):
        pass