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
        return float(token)


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
        if token in OPERATORS:
            self._binary(token)
        else:
            self.stack.append(parse_number(token))

    def _binary(self, token):
        y = self.stack.pop()
        x = self.stack.pop()
        if token == "/" and y == 0:
            raise StackMachineError(f"деление на ноль: {x} / {y}")
        self.stack.append(normalize(OPERATORS[token](x, y)))


def evaluate(expression):
    """Вычислить выражение и вернуть результат."""
    machine = StackMachine()
    for token in expression.split():
        machine.step(token)
    return machine.stack[0]
