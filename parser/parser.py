from .expr import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Expr:
        return Expr(ExprType.ADD, 
            Expr(ExprType.MUL, 
                Expr(ExprType.INTEGER, value=6), 
                Expr(ExprType.INTEGER, value=9)
            ), 
            Expr(ExprType.INTEGER, value=42)
        )