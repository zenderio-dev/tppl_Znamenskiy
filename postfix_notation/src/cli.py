"""Работа с командной строкой: аргументы, вывод шагов и ошибок."""

import glob
import os
import sys

from src.machine import StackMachineError, evaluate

USAGE = """Стековая машина для выражений в постфиксной нотации.

Использование:
    python3 main.py <выражение>

Операции: + - * / ~ (числа и операции разделяются пробелами)

Примеры:
    python3 main.py 3 0 4 ~ 2 ~
    python3 main.py 2 2 + 4 - 4 ~ 2 3 * +
"""

HINT = (
    "Подсказка: числа и операции разделяются пробелами, "
    "например: python3 main.py 3 4 +"
)


def restore_shell_symbols(args):
    """Вернуть ~ и *, которые терминал подменил до запуска программы.

    Без кавычек bash заменяет ~ на путь к домашней папке,
    а * - на список файлов в текущей папке.
    """
    home = os.path.expanduser("~")
    files = sorted(glob.glob("*"))
    result = []
    i = 0
    while i < len(args):
        if args[i] == home:
            result.append("~")
            i += 1
        elif files and sorted(args[i:i + len(files)]) == files:
            result.append("*")
            i += len(files)
        else:
            result.append(args[i])
            i += 1
    return result


def main(args):
    if not args:
        print("Вы не передали выражение - покажу, как мной пользоваться.\n")
        print(USAGE)
        return 1
    if args[0] in ("-h", "--help"):
        print(USAGE)
        return 0

    expression = " ".join(restore_shell_symbols(args))
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
