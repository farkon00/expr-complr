from .token import *
from error import throw_error

class Lexer:
    OPERATIONS = ("+", "-", "*", "/", "%", "^")

    def __init__(self, text):
        self.text = text
        self.index = 0
        self.tokens = []

    def _advance(self):
        self.index += 1
        while self.index < len(self.text) and self.text[self.index].isspace():
            self.index += 1
        if self.index >= len(self.text):
            return ""
        return self.text[self.index]

    def _unadvance(self):
        if self.index >= len(self.text):
            return ""
        self.index -= 1
        while self.index > 0 and self.text[self.index].isspace():
            self.index -= 1
        return self.text[self.index]

    def _peek(self):
        return self.text[self.index] if self.index < len(self.text) else ""

    def _lex_integer(self) -> int:
        res = 0
        while self._peek().isdigit():
            res = 10 * res + int(self._peek())
            self._advance()

        self._unadvance()

        return res

    def lex(self) -> list[Token]:
        while self.index < len(self.text):
            if self._peek().isdigit():
                self.tokens.append(Token(TokenType.INTEGER, self._lex_integer(), self.index))
            elif self._peek() in self.OPERATIONS:
                self.tokens.append(Token(TokenType.OPERATION, self._peek(), self.index))
            else:
                throw_error(f"Unknown character {self._peek()}", lexer=self)
            self._advance()
        return self.tokens