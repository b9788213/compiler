from src.lexer import lex
from src.fileman import tokenfile, src

tokens = list(lex(src))

with open(tokenfile, "w") as f: f.write("\n".join(str(t) for t in tokens))
#with open(outfile, 'w') as f: f.write()