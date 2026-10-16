class StackMachineError(Exception):
    """Ошибка вычисления с понятным для человека сообщением."""


OPERATORS = ("+", "-", "*", "/")


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
        )


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
        if token == "+":
            result = x + y
        elif token == "-":
            result = x - y
        elif token == "*":
            result = x * y
        else:
            if y == 0:
                raise StackMachineError(f"деление на ноль: {x} / {y}")
            result = x / y
        self.stack.append(normalize(result))

    def _tilde(self):
        x, y = self._pop_two("~")
        if x != 0 and y != 0:
            self.stack.append(abs(x - y))
        else:
            total = sum(self.stack) + x + y # сумма всего стека вместе с извлечёнными операндами, в квадрате
            self.stack = [normalize(total ** 2)]


def evaluate(expression):
    """Вычислить выражение.

    Возвращает результат и список шагов: (токен, стек после него).
    """
    tokens = expression.split()
    if not tokens:
        raise StackMachineError("выражение пустое, вычислять нечего")

    machine = StackMachine()
    steps = []
    for token in tokens:
        machine.step(token)
        steps.append((token, list(machine.stack)))

    if len(machine.stack) != 1:
        raise StackMachineError(
            f"в конце в стеке должно остаться одно число, а осталось {machine.stack}. "
            "Похоже, не хватает операции"
        )
    return machine.stack[0], steps
