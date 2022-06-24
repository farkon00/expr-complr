from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ExprType(Enum):
    INTEGER = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()

@dataclass
class Expr:
    TWO_SIDE_OPER = (ExprType.ADD, ExprType.SUB, ExprType.MUL, ExprType.DIV, ExprType.MOD, ExprType.POW,)
    type: ExprType
    left: Optional["Expr"] = None
    right: Optional["Expr"] = None
    value: int | str | None = None

    def _pad(self, text: str) -> str:
        return "\n".join(['  ' + i for i in text.split('\n')])

    def __str__(self) -> str:
        if self.type == ExprType.INTEGER:
            return f"{self.value}"
        elif self.type in self.TWO_SIDE_OPER:
            return f"{self.type.name}\n{self._pad(str(self.left))}\n{self._pad(str(self.right))}"
        else:
            assert False, "Unknown expression type in Expr.__str__"