from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    OPERATION = auto() 

@dataclass
class Token:
    type: TokenType
    value: str
    index: int