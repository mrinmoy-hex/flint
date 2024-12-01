from token_types import TokenType

class Token:
    """
    Represents a single token in the Tachyon programming language.

    params:
        type_ (TokenType): The type of the token (e.g., identifier, keyword, operator).
        lexeme (str): The actual string representation of the token from the source code.
        literal (object): The literal value of the token, if applicable (e.g., number or string values).
        line (int): The line number in the source code where the token appears.

    Methods:
        __str__(): Returns a formatted string representation of the token for debugging and logging purposes.
    """
    def __init__(self, type_: TokenType, lexeme: str, literal: object, line: int):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type}({self.lexeme}, {self.literal})"