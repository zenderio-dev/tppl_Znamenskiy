"""Запуск: python3 main.py 3 0 4 ~ 2 ~"""

import sys

from src.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
