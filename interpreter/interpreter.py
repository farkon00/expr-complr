from error import throw_error
from parser.expr import Expr, ExprType

class Interpreter:
    def __init__(self):
        self.prev_result = None
        self.chained = False

    def reload(self, res: int | None):
        self.prev_result = res if res is not None else self.prev_result
        self.chained = False

    def compute(self, expr: Expr, text: str = "") -> int:
        if expr.type == ExprType.INTEGER:
            return expr.value
        elif expr.type == ExprType.ADD:
            return self.compute(expr.left, text) + self.compute(expr.right, text)
        elif expr.type == ExprType.SUB:
            return self.compute(expr.left, text) - self.compute(expr.right, text)
        elif expr.type == ExprType.MUL:
            return self.compute(expr.left, text) * self.compute(expr.right, text)
        elif expr.type == ExprType.DIV:
            return self.compute(expr.left, text) // self.compute(expr.right, text)
        elif expr.type == ExprType.MOD:
            return self.compute(expr.left, text) % self.compute(expr.right, text)
        elif expr.type == ExprType.POW:
            return self.compute(expr.left, text) ** self.compute(expr.right, text)
        elif expr.type == ExprType.CHAIN:
            if self.chained or self.prev_result is None:
                throw_error("Missing left operand", index=expr.token.index, line=text)
            else:
                self.chained = True
                return self.prev_result
        else:
            assert False, f"Unknown expression type {expr.type.name}"