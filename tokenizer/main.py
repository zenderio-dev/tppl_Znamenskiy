import sys
from pathlib import Path

from lexer import Lexer, LexicalError


def main(args):
    if len(args) != 1:
        print("Usage: python main.py <file>", file=sys.stderr)
        return 1

    filename = args[0]
    try:
        source = Path(filename).read_text(encoding="utf-8")
        tokens = Lexer(source).tokenize()
    except (OSError, UnicodeError) as error:
        print(f"{filename}:1:1: lexical: {error}", file=sys.stderr)
        return 1
    except LexicalError as error:
        print(f"{filename}:{error.line}:{error.column}: lexical: {error}", file=sys.stderr)
        return 1

    for token in tokens:
        print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
