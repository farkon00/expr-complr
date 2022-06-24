from .token import *

class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.tokens = []

    def advance(self):
        self.index += 1
        while self.index < len(self.text) and self.text[self.index].isspace():
            self.index += 1
        return self.text[self.index]

    def peek(self):
        return self.text[self.index]

    def lex(self) -> list[Token]:
        return [Token(TokenType.INTEGER, "69", 0)]