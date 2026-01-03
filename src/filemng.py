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

src = infile.read_text(encoding="utf-8")


def save(ast, asm):
    astfile.write_text(get_ast(ast), encoding="utf-8")
    outfile.write_text(asm, encoding="utf-8")


def save_token(tokens):
    with open(tokenfile, "a", encoding="utf-8") as f:
        f.write("\n".join(str(t) for t in tokens))


def get_import(p: Path, name: str):
    file = (p / name).with_suffix(".txt")
    return file.parent, file.read_text()
