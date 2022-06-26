from error import throw_error
from lexer.token import Token, TokenType
from .expr import *


class Parser:
    OPER_TO_EXPR = {
        "+" : ExprType.ADD,
        "-" : ExprType.SUB,
    }
    HIGHER_OPER_TO_EXPR = {
        "*" : ExprType.MUL,
        "/" : ExprType.DIV,
        "%" : ExprType.MOD
    }

    def __init__(self, tokens: list[Token], text: str):
        self.text = text
        self.tokens = iter(tokens[::-1])
        self.last_value = None

    def parse_expr(self, is_brack: bool = False) -> Expr:
        entered = False

        final_tokens = []

        self.last_value = None

        for token in self.tokens:
            if token.type == TokenType.R_PAREN:
                final_tokens.append(self.parse_expr(is_brack=True))
            elif token.type == TokenType.L_PAREN:
                if is_brack:
                    break
                else:
                    throw_error("Parenthesis was not closed", index=token.index, line=self.text)
            else:
                final_tokens.append(token)
        else:
            if is_brack:
                throw_error("Unexpected \")\"", line=self.text)
        
        self.last_value = None
        self.tokens = iter(final_tokens)
        final_tokens = []
        for token in self.tokens:
            if self.last_value is None:
                self.last_value = token
                continue
            if token.value == "^":
                if self.last_value is None:
                    throw_error("Missing right operand", index=token.index, line=self.text)
                right = self.last_value
                if isinstance(self.last_value, Token):
                    if self.last_value.type != TokenType.INTEGER:
                        throw_error("Missing right operand", index=token.index, line=self.text)
                    right = Expr(ExprType.INTEGER, value=int(self.last_value.value))
                try:
                    left = next(self.tokens)
                except StopIteration:
                    throw_error("Missing left operand", index=token.index, line=self.text)
                if isinstance(left, Token) and left.type != TokenType.INTEGER:
                    throw_error("Missing left operand", index=left.index, line=self.text)
                if isinstance(left, Token):
                    left = Expr(ExprType.INTEGER, value=int(left.value))
                self.last_value = Expr(ExprType.POW, left, right)
            else:
                final_tokens.append(self.last_value)
                self.last_value = token

        if self.last_value is not None:
            final_tokens.append(self.last_value)
        self.last_value = None
        self.tokens = iter(final_tokens)
        final_tokens = []
        for token in self.tokens:
            if self.last_value is None:
                self.last_value = token
                continue
            if token.value in self.HIGHER_OPER_TO_EXPR:
                if self.last_value is None:
                    throw_error("Missing right operand", index=token.index, line=self.text)
                right = self.last_value
                if isinstance(self.last_value, Token):
                    if self.last_value.type != TokenType.INTEGER:
                        throw_error("Missing right operand", index=token.index, line=self.text)
                    right = Expr(ExprType.INTEGER, value=int(self.last_value.value))
                try:
                    left = next(self.tokens)
                except StopIteration:
                    throw_error("Missing left operand", index=token.index, line=self.text)
                if isinstance(left, Token):
                    if left.type != TokenType.INTEGER:
                        throw_error("Missing left operand", index=left.index, line=self.text)    
                    self.last_value = Expr(self.HIGHER_OPER_TO_EXPR[token.value], Expr(ExprType.INTEGER, value=int(left.value)), right)
                else:
                    self.last_value = Expr(self.HIGHER_OPER_TO_EXPR[token.value], left, right)
            else:
                final_tokens.append(self.last_value)
                self.last_value = token

        if self.last_value is not None:
            final_tokens.append(self.last_value)
        self.last_value = None
        self.tokens = iter(final_tokens)
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
                    if token.value != "-":
                        throw_error("Missing left operand", index=token.index, line=self.text)
                    else:
                        self.last_value.left = Expr(ExprType.INTEGER, value=0)
            elif isinstance(token, Expr):
                self.last_value = token
            else:
                assert False, f"Unknown token type {token.type.name}"

        return self.last_value if entered else None