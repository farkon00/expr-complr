from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    OPERATION = auto()
    L_PAREN = auto()
    R_PAREN = auto() 

@dataclass
class Token:
    type: TokenType
    value: str
    index: int