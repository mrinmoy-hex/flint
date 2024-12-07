from lox.token_types import TokenType
from typing import List
from lox.ast.expr import *
from tools import raise_error

class Parser:
    def __init__(self, tokens: List['Token']) -> None:
        """
        Initializes the Parser with a list of tokens
        """
        self.tokens = tokens   
        self.current = 0       # tracks the current pos in the token list
        

    @property
    def tokens(self) -> List['Token']:
        """
        Provides read-only access to the tokens.
        """
        return self.tokens
    
    
    
    def expression(self) -> 'Expr':
        """
        Parses and returns an expression.
        """
        return self.equality()
    
    
    
    def equality(self) -> 'Expr':
        """
        Parses an equality expression, handling binary operations with '!=' and '=='.
        """
        
        expr = self.comparision()
        
        while self.match(TokenType.EXCLAMATION_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparision()
            expr = Binary(expr, operator, right)
        
        return expr
    
    
    def comparision(self):
        expr = self.term()
        
        while self.match(TokenType.GREATER_THAN, TokenType.GREATER_THAN_EQUAL, TokenType.LESS_THAN, TokenType.LESS_THAN_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)    # for maintaining left associativity
            
        return expr
            
    
    
    
    ########################################
    # Methods
    ########################################
    
    
    def match(self, *types: str) -> bool:
        """
    Checks if the current token matches any of the given types. 
    If a match is found, advances the token pointer.

    Args:
        types (str): The token types to check against.

    Returns:
        bool: True if a match is found, False otherwise.
        """
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    
    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    
    def is_at_end(self) -> bool:
        """
        Checks if the parser has reached the end of the token list
        """
        return self.peek().type == TokenType.EOF
    
    
    def peek(self) -> 'Token':
        """
        Returns the current token without advancing the pos
        """
        return self.tokens[self.current]
    
    
    
    def previous(self) -> 'Token':
        """
        Returns the most recently consumed token
        """
        return self.tokens[self.current - 1]
    
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        else:
            raise self.error(self.peek(), message)
        
        
    
    def error(self, token, message):
        raise_error.error(token, message)
        return ParseError()
        
    
    
    #########################################
    # Imp. methods
    #########################################
    
    
    def term(self):
        expr = self.factor()
        
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
            
        return expr
    
    
    def factor(self):
        expr = self.unary()
        
        while self.match(TokenType.ASTERISK, TokenType.FORWARD_SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
            
        return expr
    
    
    def unary(self):
        if self.match(TokenType.EXCLAMATION, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = Unary(operator, right)    
            return expr
        
        return self.primary()
    
    
    def primary(self):
        
        if self.match(TokenType.KEYWORD_FALSE):
            return Literal(False)
        if self.match(TokenType.KEYWORD_TRUE):
            return Literal(True)
        if self.match(TokenType.KEYWORD_NIL):
            return Literal(None)
        
        
        if self.match(TokenType.NUMBER_LITERAL, TokenType.STRING_LITERAL):
            return Literal(self.previous().literal)
        
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr
    

        
        
        
    