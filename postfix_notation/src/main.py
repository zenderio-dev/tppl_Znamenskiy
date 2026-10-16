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


def format_stack(stack):
    return "[" + ", ".join(str(value) for value in stack) + "]"


def print_step(token, stack):
    print(f"  {token:>6}  ->  {format_stack(stack)}")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv

    if not args:
        print("Вы не передали выражение - покажу, как мной пользоваться.\n")
        print(USAGE)
        return 1
    if args[0] in ("-h", "--help"):
        print(USAGE)
        return 0

    expression = " ".join(args)
    print(f"Вычисляю: {expression}")
    try:
        result = evaluate(expression, on_step=print_step)
    except StackMachineError as error:
        print(f"Не получилось вычислить: {error}", file=sys.stderr)
        print(HINT, file=sys.stderr)
        return 1

    print(f"{expression} = {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
