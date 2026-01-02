from typing import NoReturn
import node as n
from lexer import Token, lex
from filemng import get_import
from pathlib import Path

class Parser:
    def __init__(self, name: Path, tokens: list[Token]):
        self.name = name
        self.tokens = tokens
        self.index: int = 0
        self.p = n.Program()
        self.currentf: n.Func = None

    #-----Helpers-----
    def peek(self, n=0):
        return self.tokens[self.index + n]

    def pop(self):
        t = self.tokens[self.index]
        self.index += 1
        return t

    def expect(self, s):
        t = self.pop()
        if t.type != s: raise SyntaxError(f"Expected {s}, but got ({t}).")
        return t.value

    def check(self, s) -> bool:
        return self.peek().type == s

    def match(self, s) -> bool:
        if self.check(s):
            self.pop()
            return True
        return False

    def error(self) -> NoReturn:
        raise SyntaxError(f"Bad Token ({self.peek()})")

    #-----entry-----
    def parse(self):
        while not self.match('EOF'):

            if self.match("IMPORT"):
                path = "/".join(self.dot())
                self.handle_import(path)
                continue

            if self.match("FN"):
                f = self.parse_func()
                self.p.funcs.append(f)
                continue

            self.error()

        return self.p

    #-----func-----
    def parse_func(self) -> n.Func:
        name = self.expect("ID")

        
        f = n.Func(name)
        self.currentf = f

        self.expect("LPAR")
        f.args = self.parse_list(lambda: self.expect("ID"))
        self.expect("RPAR")

        f.body = self.getbody()

        return f

    #-----stmt-----
    def parse_stmt(self):

        if self.match("ASM"):
            asms = [self.expect("STR")]

            while self.peek().type == "STR": asms.append(self.pop().value)

            self.expect("ASM")
            return n.Asm("\n".join(asms))

        if self.match("IF"):
            ifs = [n.If(self.compare(), self.getbody())]
            elsebody = None

            while self.match("ELIF"):
                ifs.append(n.If(self.compare(), self.getbody()))

            if self.match("ELSE"):
                elsebody = self.getbody()

            if elsebody: return n.ConditionelStruct(ifs, elsebody)
            return n.ConditionelStruct(ifs)

        if self.match("WHILE"):
            return n.While(self.compare(), self.getbody())

        if self.check("ID"):
            name = self.pop().value

            #call
            if self.match("LPAR"):
                return self.parse_call(name)

            #assign and declaration
            if self.match("EQ"):
                self.currentf.vars[name] = 0
                return n.Assign(name, self.compare())

        #Static decleration
        if self.match("STATIC"):
            name = self.expect("ID")
            self.p.statics.append(Id(name))
            self.expect("EQ")
            return n.Assign(name, self.compare())

        if self.match("RET"):
            return n.Ret(self.compare())

        self.error()

    #-----presedence-----
    def compare(self):
        node = self.expr()

        while self.peek().type in ("EQEQ", "NEQ", "LEQ", "GEQ", "LT", "GT"):
            op = self.pop().type
            node = n.Comp(op, node, self.expr())
        return node

    def expr(self):
        node = self.term()

        while self.peek().type in ("PLUS", "MINUS"):
            op = self.pop().type
            node =  n.BinOp(op, node, self.term())
        return node

    def term(self):
        node = self.factor()

        while self.peek().type in ("MUL", "DIV", "MOD"):
            op = self.pop().type
            node = n.BinOp(op, node, self.factor())
        return node

    def factor(self):
        if self.match("LPAR"):
            node = self.compare()  # En başa dön!
            self.expect("RPAR")
            return node

        if self.match("MINUS"): return n.Neg(self.factor())

        if self.check("INT"): return n.Int(int(self.pop().value))

        if self.check("FLOAT"): return n.Float(float(self.pop().value))

        if self.check("STR"): return n.String(self.pop().value)

        if self.check("ID"):
            name = self.pop().value
            if self.match("LPAR"): return self.parse_call(name)
            return Id(name)

        self.error()

    def dot(self):
        ids = [self.expect("ID")]

        while self.match("DOT"):
            ids.append(self.expect("ID"))

        return ids

    #-----call-----
    def parse_call(self, name: str):
        args = self.parse_list(self.compare)
        self.expect("RPAR")
        return n.Call(name, args)

    def getbody(self) -> n.Body:
        self.expect("COLON")
        self.expect("INDENT")
        b = n.Body()

        while not self.match("DEDENT"): b.code.append(self.parse_stmt())

        return b

    #-----list-----
    def parse_list(self, parser_f) -> list:
        elements = []

        if self.check("RPAR"): return elements

        elements.append(parser_f())

        while self.match("COMMA"): elements.append(parser_f())

        return elements

    def handle_import(self, impname: str):
        parent, file = get_import(self.name, impname)

        tokens = list(lex(file))
        ast = Parser(parent, tokens).parse()

        self.p.funcs.extend(ast.funcs)
        self.p.statics.extend(ast.statics)


