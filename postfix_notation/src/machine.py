"""Стековая машина для выражений в постфиксной нотации."""


class StackMachine:
    def __init__(self):
        self.stack = []

    def step(self, token):
        """Обработать один токен: число кладём в стек, операцию выполняем."""
        if token == "+":
            y = self.stack.pop()
            x = self.stack.pop()
            self.stack.append(x + y)
        else:
            self.stack.append(int(token))


def evaluate(expression):
    """Вычислить выражение и вернуть результат."""
    machine = StackMachine()
    for token in expression.split():
        machine.step(token)
    return machine.stack[0]
