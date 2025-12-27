from codegen import CodeGen
from filemng import src, save
from lexer import lex
from parser import Parser

tokens = list(lex(src))

ast = Parser(tokens).parse()

asm = CodeGen(ast).gen()

save(tokens, ast, asm)