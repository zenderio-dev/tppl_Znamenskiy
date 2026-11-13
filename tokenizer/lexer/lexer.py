from .token import Token, TokenType


KEYWORDS = {"if", "else", "while", "return", "for", "def"}
OPERATORS = {"+", "-", "*", "/", "=", "<", ">", "==", "<=", ">="}
SEPARATORS = {"(", ")", "{", "}", ",", ";"}
DIGITS = set("0123456789")


class LexicalError(Exception):
    def __init__(self, line, column, message):
        super().__init__(message)
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

    def peek(self, offset=0):
        return self.text[self.pos + offset:self.pos + offset + 1]

    def advance(self):
        if self.peek() == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip(self):
        while self.peek():
            if self.peek().isspace():
                self.advance()
            elif self.peek() == "#":
                while self.peek() not in ("", "\n"):
                    self.advance()
            else:
                break

    def number(self):
        while self.peek() in DIGITS:
            self.advance()
        if self.peek() == ".":
            self.advance()
            while self.peek() in DIGITS:
                self.advance()
            return TokenType.FLOAT
        return TokenType.INT

    def string(self, line, column):
        self.advance()
        while self.peek() not in ("", "\n", '"'):
            self.advance()
        if self.peek() != '"':
            raise LexicalError(line, column, "unterminated string literal")
        self.advance()

    def next(self):
        self.skip()
        char = self.peek()
        if not char:
            return None

        start = self.pos
        line, column = self.line, self.column
        if char.isalpha() or char == "_":
            while self.peek().isalnum() or self.peek() == "_":
                self.advance()
            word = self.text[start:self.pos]
            kind = TokenType.KEYWORD if word in KEYWORDS else TokenType.IDENT
        elif char in DIGITS or (char == "." and self.peek(1) in DIGITS):
            kind = self.number()
        elif char == '"':
            self.string(line, column)
            kind = TokenType.STRING
        elif char in OPERATORS:
            pair = self.text[start:start + 2]
            self.advance()
            if len(pair) == 2 and pair in OPERATORS:
                self.advance()
            kind = TokenType.OP
        elif char in SEPARATORS:
            self.advance()
            kind = TokenType.SEP
        else:
            raise LexicalError(line, column, f"unexpected character {char!r}")

        return Token(kind, self.text[start:self.pos], line, column)

    def tokenize(self):
        tokens = []
        while (token := self.next()) is not None:
            tokens.append(token)
        return tokens
