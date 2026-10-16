"""Стековая машина для выражений в постфиксной нотации."""


class StackMachineError(Exception):
    """Ошибка вычисления с понятным для человека сообщением."""


OPERATORS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
}


def parse_number(token):
    """Превратить токен в число: сначала пробуем int, потом float."""
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        raise StackMachineError(
            f"не понимаю '{token}': это не число и не операция (+ - * / ~)"
        ) from None


def normalize(value):
    """Убрать лишнее '.0' у целых результатов: 4.0 -> 4."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


class StackMachine:
    def __init__(self):
        self.stack = []

    def step(self, token):
        """Обработать один токен: число кладём в стек, операцию выполняем."""
        if token == "~":
            self._tilde()
        elif token in OPERATORS:
            self._binary(token)
        else:
            self.stack.append(parse_number(token))

    def _pop_two(self, token):
        if len(self.stack) < 2:
            raise StackMachineError(
                f"для операции '{token}' нужно два числа, "
                f"а в стеке сейчас {self.stack}"
            )
        y = self.stack.pop()
        x = self.stack.pop()
        return x, y

    def _binary(self, token):
        x, y = self._pop_two(token)
        if token == "/" and y == 0:
            raise StackMachineError(f"деление на ноль: {x} / {y}")
        self.stack.append(normalize(OPERATORS[token](x, y)))

    def _tilde(self):
        x, y = self._pop_two("~")
        if x != 0 and y != 0:
            self.stack.append(abs(x - y))
        else:
            # сумма всего стека вместе с извлечёнными операндами, в квадрате
            total = sum(self.stack) + x + y
            self.stack = [normalize(total ** 2)]


def evaluate(expression, on_step=None):
    """Вычислить выражение и вернуть результат.

    on_step(token, stack) вызывается после каждого шага -
    так можно вывести состояние стека.
    """
    tokens = expression.split()
    if not tokens:
        raise StackMachineError("выражение пустое, вычислять нечего")

    machine = StackMachine()
    for token in tokens:
        machine.step(token)
        if on_step:
            on_step(token, list(machine.stack))

    if len(machine.stack) != 1:
        raise StackMachineError(
            f"в конце в стеке должно остаться одно число, а осталось {machine.stack}. "
            "Похоже, не хватает операции"
        )
    return machine.stack[0]
