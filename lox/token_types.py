from enum import Enum, auto

class TokenType(Enum):
    """
    This class categorizes tokens into:
    - Single-character tokens (e.g., parentheses, operators).
    - One or two-character tokens (e.g., comparison operators).
    - Literals (e.g., identifiers, strings, numbers).
    - Keywords (reserved words in the language).
    - Special tokens (e.g., end-of-file).
    """

    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    FORWARD_SLASH = auto()
    ASTERISK = auto()

    # One or two character tokens
    EQUAL = auto()
    EXCLAMATION = auto()
    EXCLAMATION_EQUAL = auto()
    ASSIGN = auto()
    EQUAL_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_THAN_EQUAL = auto()
    LESS_THAN = auto()
    LESS_THAN_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING_LITERAL = auto()
    NUMBER_LITERAL = auto()

    # Keywords
    KEYWORD_AND = auto()
    KEYWORD_CLASS = auto()
    KEYWORD_ELSE = auto()
    KEYWORD_FALSE = auto()
    KEYWORD_FUNCTION = auto()
    KEYWORD_FOR = auto()
    KEYWORD_IF = auto()
    KEYWORD_NIL = auto()
    KEYWORD_OR = auto()
    KEYWORD_PRINT = auto()
    KEYWORD_RETURN = auto()
    KEYWORD_SUPER = auto()
    KEYWORD_THIS = auto()
    KEYWORD_TRUE = auto()
    KEYWORD_VARIABLE = auto()
    KEYWORD_WHILE = auto()

    # End of file
    EOF = auto()
