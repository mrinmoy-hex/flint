from flint.token_types import TokenType
from flint.ast.expr import *
from flint.ast.stmt import *
from tools import raise_error

class Parser:
    """
    A recursive descent parser for a simple language, responsible for
    converting a sequence of tokens into an Abstract Syntax Tree (AST).
    """
    def __init__(self, tokens) -> None:
        """
        Initialize the parser with a list of tokens.

        Args:
            tokens (list): A list of Token objects to be parsed.
        """
        self._tokens = tokens   
        self.current = 0       # tracks the current pos in the token list
        
        
    
    class ParseError(Exception):
        """Custom exception for error class"""
        pass
    

    @property
    def tokens(self):
        """
        Provides read-only access to the tokens.
        """
        return self._tokens
    
    
    def expression(self):
        """
        Parses and returns an expression.
        """
        return self.equality()
    
    
    def declaration(self):
        """
        Parse a declaration statement. 

        If the current token matches a variable declaration (`VAR`), 
        parse it as a variable declaration. Otherwise, parse it as a general statement.

        Returns:
            Stmt: The parsed statement object, or None if a parse error occurs.
        """
        
        try:
            # check if the current token matches a variable declaration
            if self.match(TokenType.KEYWORD_VARIABLE):
                return self.var_declaration()
            
            # if not a variable declaration, parse a general statement
            return self.statement()
        
        except self.ParseError:
            # if a parsing error occurs, recover by synchrinizing and return null
            self.synchronize()
            return None
        
        
        
        
    
    def statement(self):
        """
        Parse a single statement.

        Returns:
            Stmt: The parsed statement as an AST node.
        """
        if self.match(TokenType.KEYWORD_PRINT):
            return self.print_statement()
        return self.expression_statement()
    
    
    
    def print_statement(self):
        """
        Parse a print statement.

        This method consumes the current token as an expression to be printed,
        and ensures the statement ends with a semicolon.

        Returns:
            Print: A Print statement AST node containing the parsed expression.
        """
        value = self.expression()   # parse the expression to print
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)         # return a Print statement AST node
    
    
    
    def var_declaration(self):
        """
        Parse a variable declaration statement.

        Expects a variable name, followed optionally by an initializer 
        (if an '=' token is present), and ends with a semicolon.

        Returns:
            Stmt.Var: A variable declaration statement containing the variable's 
            name and initializer expression (or None if no initializer is provided).
        """
        
        # consume the identifier token for the variable name
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        
        # optionally parse an initializer if '=' is present
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        # ensure the statement ends with a semicolon
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        
        
        # return a new variable declaration statement node
        return Var(name, initializer)
        
    
    
    
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ',' after expression")
        return Stmt.Expression(expr)
    
    
    
    def equality(self):
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
        """
        Check if the current token matches a specific type.

        Args:
            token_type (str): The type of token to check.

        Returns:
            bool: True if the current token matches the type, False otherwise.
        """
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    
    def advance(self):
        """
        Advance the parser to the next token and return the current token.

        Returns:
            Token: The token that was advanced past.
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    
    def is_at_end(self) -> bool:
        """
        Check if the parser has reached the end of the tokens.

        Returns:
            bool: True if at the end of the token stream, False otherwise.
        """
        return self.peek().type == TokenType.EOF
    
    
    def peek(self):
        """
        Get the current token without advancing the parser.

        Returns:
            Token: The current token.
        """
        return self.tokens[self.current]
    
    
    
    def previous(self):
        """
        Get the most recently consumed token.

        Returns:
            Token: The previous token.
        """
        return self.tokens[self.current - 1]
    
    
    def consume(self, type: TokenType, message: str):
        """
        Consume the current token if it matches the expected type.

        Args:
            token_type (str): The expected type of the token.
            error_message (str): The error message to raise if the token doesn't match.

        Returns:
            Token: The consumed token.

        Raises:
            RuntimeError: If the current token does not match the expected type.
        """
        if self.check(type):
            return self.advance()
        else:
            raise self.error(self.peek(), message)
        
        
    
    def error(self, token, message):
        raise_error.error(token, message)
        raise self.ParseError()  # raise the custom ParseError
    
    
    
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
        """
        Parse a primary expression.

        Handles literals, variables, and grouped expressions enclosed in parentheses.

        Returns:
            Expr: The parsed primary expression.
        """

        
        if self.match(TokenType.KEYWORD_FALSE):
            return Literal(False)
        if self.match(TokenType.KEYWORD_TRUE):
            return Literal(True)
        if self.match(TokenType.KEYWORD_NIL):
            return Literal(None)
        
        
        if self.match(TokenType.NUMBER_LITERAL, TokenType.STRING_LITERAL):
            return Literal(self.previous().literal)
        
        # handle variable access by identifier
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr
            # return Grouping(expr)
        
        # if none above matches, we've an error
        self.error(self.peek(), "Expect expression.")
        return None
        
        
        
    ######################################################
    # Synchronization for error recovery
    ######################################################
    
    def synchronize(self):
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            if self.peek().type in {
                TokenType.KEYWORD_CLASS,
                TokenType.KEYWORD_FUNCTION,
                TokenType.KEYWORD_VARIABLE, 
                TokenType.KEYWORD_FOR,
                TokenType.KEYWORD_IF,
                TokenType.KEYWORD_WHILE,
                TokenType.KEYWORD_PRINT, 
                TokenType.KEYWORD_RETURN,
            }:
                return
            
            self.advance()
            
            
    #####################################################
    # Kick start point
    ####################################################
    
    def parse(self):
        """
        Initiates parsing and handles parse errors.
        """
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

        
        
        
    