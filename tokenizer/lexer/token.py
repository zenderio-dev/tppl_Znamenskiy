from enum import Enum, auto


class TokenType(Enum):
    IDENT = auto()
    KEYWORD = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    OP = auto()
    SEP = auto()


class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type_ = type_
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"({self.type_.name}, {self.value}, {self.line}:{self.column})"
