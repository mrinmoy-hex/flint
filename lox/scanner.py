from lox.token_types import *
from lox.token import Token
from tools import raise_error

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []    # list to store tokens

        # tracing position
        self.start = 0
        self.current = 0
        self.line = 1


    def is_at_end(self):
        return self.current >= len(self.source)



    def scan_tokens(self):
        while not self.is_at_end():
            # we are at the beginning of the next lexeme
            self.start = self.current
            self.scan_token()
            #   here we are not breaking the loop in case of error
            # i just want to consume the tokens until EOF and then report the errors all at a time

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))


    # recognizing lexeme
    def scan_token(self):
        char = self.advance()

        if char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '*':
            self.add_token(TokenType.ASTERISK)

        # for comparision operators
        elif char == '!':
            self.add_token(TokenType.EXCLAMATION_EQUAL if self.match('=') else TokenType.EXCLAMATION)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_THAN_EQUAL if self.match('=') else TokenType.LESS_THAN)
        elif char == '>':
            self.add_token(TokenType.GREATER_THAN_EQUAL if self.match('=') else TokenType.GREATER_THAN)
        else:
            raise_error.error(self.line, f"Unexpected character: {char}")



    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))



    def advance(self) -> str:
        char = self.source[self.current]    # get the current char
        self.current += 1   # move the pointer to next char
        return char



    def match(self, expected) -> bool:
        if self.is_at_end():
            return False    # at the end, nothing to match
        if self.source[self.current] != expected:
            return False    # next char doesn't match the expected one

        self.current += 1   # consume the matching char
        return True





