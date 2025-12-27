from codegen import CodeGen
from filemng import tokenfile, astfile, src
from lexer import lex
from parser import Parser
from printast import get_ast

tokens = list(lex(src))

ast = Parser(tokens).parse()

asm = CodeGen(ast).gen()

with open(tokenfile, "w") as f: f.write("\n".join(str(t) for t in tokens))
with open(astfile, "w", encoding="utf-8") as f: f.write(get_ast(ast))
#with open(outfile, 'w') as f: f.write()