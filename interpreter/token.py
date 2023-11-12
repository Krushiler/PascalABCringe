from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    ASSIGN = auto()
    BEGIN = auto()
    END = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    ID = auto()
    EOL = auto()


class Token:

    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):  # pragma: no cover
        return f"Token({self.type_}, {self.value})"
