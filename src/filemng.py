from pathlib import Path
from printast import get_ast
import sys

infile = Path(sys.argv[1]).with_suffix('.txt')
parent = infile.parent

build_dir = parent / "build"
debug_dir = parent / "debug"

debug_dir.mkdir(parents=True, exist_ok=True)
build_dir.mkdir(parents=True, exist_ok=True)

outfile = build_dir / "out.asm"
tokenfile = debug_dir / "tokens.txt"
astfile = debug_dir / "ast.txt"

with open(infile, encoding="utf-8") as f: src = f.read()

def save(tokens, ast, asm):
    with open(tokenfile, "w", encoding="utf-8") as f: f.write("\n".join(str(t) for t in tokens))
    with open(astfile, "w", encoding="utf-8") as f: f.write(get_ast(ast))
    with open(outfile, 'w', encoding="utf-8") as f: f.write(asm)

def get_import(name: str) -> str:
    return (parent / name).with_suffix(".txt").read_text()