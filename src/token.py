from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Tipe Data Dasar
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Kategori dari Pemetaan project_setup.md
    KEYWORD = auto()
    BUILTIN = auto()
    
    # Operator
    OPERATOR = auto()
    
    # Pembatas
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    
    # Akhir File
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
