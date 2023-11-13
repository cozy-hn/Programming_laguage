from enum import Enum

class TokenType(Enum):
    CONST = 1
    IDENT = 2
    ASSIGNMENT_OP = 3
    ADD_OP = 4
    MULT_OP = 5
    LEFT_PAREN = 6
    RIGHT_PAREN = 7
    SEMI_COLON = 8
    UNDEFINED = 9
    EOF = 10