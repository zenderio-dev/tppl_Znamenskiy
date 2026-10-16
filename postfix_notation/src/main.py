"""Запуск стековой машины из командной строки."""

import sys

from src.machine import StackMachineError, evaluate

USAGE = """Стековая машина для выражений в постфиксной нотации.

Использование:
    python -m src.main "<выражение>"

Операции: + - * / ~ (числа и операции разделяются пробелами)

Примеры:
    python -m src.main "3 0 4 ~ 2 ~"
    python -m src.main "2 2 + 4 - 4 ~ 2 3 * +"
"""

HINT = (
    "Подсказка: числа и операции разделяются пробелами, "
    'а выражение лучше взять в кавычки, например: python -m src.main "3 4 +"'
)


def main(args):
    if not args:
        print("Вы не передали выражение - покажу, как мной пользоваться.\n")
        print(USAGE)
        return 1
    if args[0] in ("-h", "--help"):
        print(USAGE)
        return 0

    expression = " ".join(args)
    try:
        result, steps = evaluate(expression)
    except StackMachineError as error:
        print(f"Не получилось вычислить: {error}", file=sys.stderr)
        print(HINT, file=sys.stderr)
        return 1

    for token, stack in steps:
        print(f"{token}  ->  {stack}")
    print(f"{expression} = {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
