from pathlib import Path
import sys

infile = Path(sys.argv[1]).with_suffix('.txt')

build_dir = Path(infile.parent) / "build"
debug_dir = Path(infile.parent) / "debug"

debug_dir.mkdir(parents=True, exist_ok=True)
build_dir.mkdir(parents=True, exist_ok=True)

outfile = build_dir / "out.asm"
tokenfile = debug_dir / "tokens.txt"
astfile = debug_dir / "ast.txt"

with open(infile) as f: src = f.read()