from lox.token import Token
from lox.token_types import *
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
            self.start = self.current       # -> points to the start of next lexeme
            self.scan_token()

            #   here we are not breaking the loop in case of error
            # I just want to consume the tokens until EOF and then report the errors all at a time

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        
        return self.tokens


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

        elif char == '/':
            if self.match('/'):
                # a comment goes until the line ends
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
                    # No token is added for comments, as they are ignored.
                    
                    
            # support for multiline comments
            elif self.match('*'):
                self.scan_multiline_comment()
                    
                    
                    # self.current += 1
            
            else:
                self.add_token(TokenType.FORWARD_SLASH)
                
        

        elif char in {' ', '\r', '\t'}:
            # ignore white spaces
            pass

        elif char == '\n':
            # increments the line number
            self.line += 1


        # for comparision operators
        elif char == '!':
            self.add_token(TokenType.EXCLAMATION_EQUAL if self.match('=') else TokenType.EXCLAMATION)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_THAN_EQUAL if self.match('=') else TokenType.LESS_THAN)
        elif char == '>':
            self.add_token(TokenType.GREATER_THAN_EQUAL if self.match('=') else TokenType.GREATER_THAN)


        # handling sting literals
        elif char == '"':
            self.string()

        # handling number literals
        elif self.is_digit(char):
            self.number()

        # support for reserved keywords
        elif self.is_alpha(char):
            self.indentifier()

        else:
            raise_error.error(self.line, f"Unexpected character: {char}")



    ###################################################################3
    # Methods
    ###################################################################

    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
        # print(self.tokens[0])



    def advance(self) -> str:
        if self.is_at_end():
            return '\0'     # returns a null character to handle end of input
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

    def peek(self):
        if self.is_at_end():
            return '\0'     # returns NULL
        return self.source[self.current]    # char lookahed


    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1      # handles new line breaks in the string variable -> multi-line strings
            self.advance()

        if self.is_at_end():
            raise_error.error(self.line, "Unterminated string.")
            return

        # the closing "
        self.advance()

        # trimming the surrounding quotes
        value = self.source[self.start+1: self.current - 1]
        self.add_token(TokenType.STRING_LITERAL, value)


    def is_digit(self, c):
        return c.isdigit()

    def number(self):
        # Record the starting point of the token.
        start = self.current - 1
        
        has_decimal = False

        while self.is_digit(self.peek()):
            self.advance()  # process the int part

        # Look for the fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()
            has_decimal = True

            while self.is_digit(self.peek()):
                self.advance()

        
        # Ensure there's no second decimal point.
        if has_decimal and not self.is_digit(self.peek()):
            raise_error.error(self.line, "Invalid number format: trailing decimal point")
            return


        # convert the number string into float
        value = self.source[start:self.current]
        try:
            number_value = float(self.source[start: self.current])
            # print(number_value)
            self.add_token(TokenType.NUMBER_LITERAL, number_value)
        except ValueError:
            raise_error.error(self.line, f"Invalid number: {value}")


    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]



    def indentifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        # Extract the full identifier or keyword text
        text = self.source[self.start:self.current]

        # Check if it's a reserved keyword; otherwise, treat as an identifier
        token_type = self.KEYWORDS.get(text, TokenType.IDENTIFIER)

        # Add the token for the keyword or identifier
        self.add_token(token_type)



    def is_alpha(self, char):
        """Check if the character is an alphabet or an underscore."""
        return char.isalpha() or char == '_'


    def is_alphanumeric(self, char):
        """Check if the char is a letter, digit or underscore"""
        return  self.is_alpha(char) or self.is_digit(char)


    # reserved keywords
    KEYWORDS = {
        "and": TokenType.KEYWORD_AND,
        "class": TokenType.KEYWORD_CLASS,
        "else": TokenType.KEYWORD_ELSE,
        "false": TokenType.KEYWORD_FALSE,
        "for": TokenType.KEYWORD_FOR,
        "fn": TokenType.KEYWORD_FUNCTION,
        "if": TokenType.KEYWORD_IF,
        "nil": TokenType.KEYWORD_NIL,
        "or": TokenType.KEYWORD_OR,
        "print": TokenType.KEYWORD_PRINT,
        "return": TokenType.KEYWORD_RETURN,
        "super": TokenType.KEYWORD_SUPER,
        "this": TokenType.KEYWORD_THIS,
        "true": TokenType.KEYWORD_TRUE,
        "var": TokenType.KEYWORD_VARIABLE,
        "while": TokenType.KEYWORD_WHILE,
    }
    
    
    def scan_multiline_comment(self):
        # Ensure we encounter '/*' before entering the comment.
        # if not self.ma:
        #     raise_error.error(self.line, "Unexpected character in comment start.")
            
            
        while True:
            if self.is_at_end():  # If we reach the end of the input, the comment is unterminated.
                raise_error.error(self.line, "Unterminated comment.")
                return

            # if self.peek() == '*' and self.peek_next() == '/':  # look ahead to check for */
            #     self.advance()
            #     self.advance()
            #     return  # comment ended
            
            
            # look ahead for '*/' to terminate the comment
            if self.match('*') and self.match('/'):
                return      # end the comment
            
            

            if self.peek() == '\n':
                self.line += 1
                
            self.advance()      # consume the character
            





