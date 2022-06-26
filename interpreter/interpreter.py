from parser.expr import Expr, ExprType

class Interpreter:
    def compute(self, expr: Expr):
        if expr.type == ExprType.INTEGER:
            return expr.value
        elif expr.type == ExprType.ADD:
            return self.compute(expr.left) + self.compute(expr.right)
        elif expr.type == ExprType.SUB:
            return self.compute(expr.left) - self.compute(expr.right)
        elif expr.type == ExprType.MUL:
            return self.compute(expr.left) * self.compute(expr.right)
        elif expr.type == ExprType.DIV:
            return self.compute(expr.left) // self.compute(expr.right)
        elif expr.type == ExprType.MOD:
            return self.compute(expr.left) % self.compute(expr.right)
        elif expr.type == ExprType.POW:
            return self.compute(expr.left) ** self.compute(expr.right)
        else:
            assert False, f"Unknown expression type {expr.type.name}"