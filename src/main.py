from codegen import CodeGen
from filemng import src, save, parent
from lexer import lex
from parser import Parser

tokens = lex(src)

ast = Parser(parent, tokens).parse()

asm = CodeGen(ast).gen()

save(ast, asm)
