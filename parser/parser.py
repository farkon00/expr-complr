from error import throw_error
from lexer.token import Token, TokenType
from .expr import *

class Parser:
    OPER_TO_EXPR = {
        "+" : ExprType.ADD,
        "-" : ExprType.SUB,
        "*" : ExprType.MUL,
        "/" : ExprType.DIV,
        "%" : ExprType.MOD,
        "^" : ExprType.POW,
    }

    def __init__(self, tokens: list[Token], text: str):
        self.text = text
        self.tokens = iter(tokens[::-1])
        self.last_value = None

    def parse_expr(self) -> Expr:
        entered = False
        for token in self.tokens:
            entered = True
            if token.type == TokenType.INTEGER:
                self.last_value = Expr(ExprType.INTEGER, value=token.value)
            elif token.type == TokenType.OPERATION and token.value in self.OPER_TO_EXPR:
                if self.last_value is None:
                    throw_error("Missing right operand", index=token.index, line=self.text)
                right = self.last_value
                self.last_value = Expr(self.OPER_TO_EXPR[token.value], self.parse_expr(), right)
                if self.last_value.left is None:
                    throw_error("Missing left operand", index=token.index, line=self.text)
            else:
                assert False, f"Unknown token type {token.type.name}"

        return self.last_value if entered else None