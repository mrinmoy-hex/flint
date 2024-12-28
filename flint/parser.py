from flint.token_types import TokenType
from flint.ast.expr import *
from flint.ast.stmt import *
from tools import raise_error

class Parser:
    """
    Parser class for parsing a list of tokens into an Abstract Syntax Tree (AST).
    Attributes:
        _tokens (list): A list of Token objects to be parsed.
        current (int): Tracks the current position in the token list.
    Inner Classes:
        ParseError: Custom exception for parsing errors.
    """
    
    def __init__(self, tokens, is_repl_mode) -> None:
        """
        Initialize the parser with a list of tokens.

        Args:
            tokens (list): A list of Token objects to be parsed.
        """
        self._tokens = tokens   
        self.current = 0       # tracks the current pos in the token list
        self.is_repl_mode = is_repl_mode
        
        
    
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
        return self.assignment()
    
    
    def declaration(self):
        """
        Parse a declaration statement. 

        If the current token matches a variable declaration (`VAR`), 
        parse it as a variable declaration. Otherwise, parse it as a general statement.

        Returns:
            Stmt: The parsed statement object, or None if a parse error occurs.
        """
        
        try:
            # check if the current token matches a function declaration
            if self.match(TokenType.KEYWORD_FUNCTION):
                return self.function("function")
            
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
        
        if self.match(TokenType.KEYWORD_FOR):
            return self.for_statement()
        
        if self.match(TokenType.KEYWORD_IF):
            return self.if_statement()
        
        if self.match(TokenType.KEYWORD_WHILE):
            return self.while_statement()
        
        if self.match(TokenType.KEYWORD_PRINT):
            return self.print_statement()
        
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        
        return self.expression_statement()
    
    
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        
        # parse the initializer
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.KEYWORD_VARIABLE):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()    
            
        # parse the condition
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        
        
        # parse the increment
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        
        # parse the body (loop body)
        body = self.statement()
        
        # Desugar into a while loop
        # If there's an increment, append it to the body
        if increment is not None:
            body = Block([body, Expression(increment)])
            
        # if no condition is specified, use `True` as the default condition
        if condition is None:
            condition = Literal(True)
        body = While_stmt(condition, body)
        
        # if there's an initializer, execute it before the loop
        if initializer is not None:
            body = Block([initializer, body])
        
        return body
        
    
    
    
    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.KEYWORD_ELSE):
            else_branch = self.statement()
        
        return If_stmt(condition, then_branch, else_branch)
    
    
    
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
    
        
    
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        
        return While_stmt(condition, body)
    
    
        
    
    
    def expression_statement(self):
        """
        Parses an expression statement in the source code.

        This method expects an expression followed by a semicolon.
        It consumes the semicolon token and returns an Expression statement.

        Returns:
            Stmt.Expression: An expression statement object.

        Raises:
            ParseError: If the semicolon is not found after the expression.
        """
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        
        if self.is_repl_mode:  # Automatically print results in REPL mode
            return Print(expr)
        
        return Expression(expr)
    
    
    def function(self, kind):
        """
        Parse a funtion declaration.
        """
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        
        parameters = []        
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
                
                # check if there are more parameters
                if not self.match(TokenType.COMMA):
                    break
                
        # consume the closing parenthesis        
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{ ' before {kind} body.")
        body = self.block()
        
        return Function(name, parameters, body)     # return a function statement
    
    
    
    def block(self):
        """
        Parses a block of code enclosed in braces and returns a list of statements.
        This method continues to parse declarations and add them to the statements
        list until it encounters a right brace or reaches the end of the input.
        Returns:
            list: A list of parsed statements within the block.
        Raises:
            ParseError: If the right brace '}' is not found after the block.
        """
        statements = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
            
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    
    
    def assignment(self):
        expr = self.or_logic()
        
        if self.match(TokenType.EQUAL):
            equals = self.previous()                            # store the = token
            value = self.assignment()                           # recursively parse the right-hand side of assignment
            
            if isinstance(expr, Variable):  
                name = expr.name
                return Assign(name, value)                      # return an assign expression with a variable and a value
            
            self.error(equals, "Invalid assignment target.")    # throws an error if it's not a valid target
            
        return expr                                             # returns the original expression if there's no assignment
            
        
    def or_logic(self):
        expr = self.and_logic()
        
        while self.match(TokenType.KEYWORD_OR):
            operator = self.previous()
            right = self.and_logic()
            expr = Logical(expr, operator, right)   # follows left-associative structure
            
        return expr
        
    
    def and_logic(self):
        expr = self.equality()
        
        while self.match(TokenType.KEYWORD_AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
            
        return expr
        
    
    
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
        """
        Parses and returns a comparison expression.
        This method handles comparison operators such as greater than, greater than or equal to,
        less than, and less than or equal to. It maintains left associativity by constructing
        a binary expression tree.
        Returns:
            expr: The parsed comparison expression.
        """
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
        """
        Handles parsing errors by raising a custom ParseError.

        Args:
            token: The token where the error occurred.
            message: A description of the error.

        Raises:
            self.ParseError: Custom exception indicating a parsing error.
        """
        raise_error.error(token, message)
        raise self.ParseError()  # raise the custom ParseError
    
    
    
    #########################################
    # Imp. methods
    #########################################
    
    def binary_expr(self, sub_expr_method, *operators):
        """
        Parse a binary expression.
    
        Args:
            sub_expr_method (callable): The method to parse the sub-expressions (e.g., self.unary).
            operators (TokenType): The binary operators to handle at this level.

            Returns:
            Expr: The parsed binary expression or a single sub-expression.
        """
        expr = sub_expr_method()

        while self.match(*operators):
            operator = self.previous()
            right = sub_expr_method()
            expr = Binary(expr, operator, right)

        return expr
    
    
    def term(self):
        return self.binary_expr(self.factor, TokenType.PLUS, TokenType.MINUS)

    
    
    def factor(self):
        return self.binary_expr(self.unary, TokenType.ASTERISK, TokenType.FORWARD_SLASH)
    
    
    def unary(self):
        if self.match(TokenType.EXCLAMATION, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = Unary(operator, right)    
            return expr
        
        return self.call()
    
    
    def call(self):
        """
        Parse a call expression.
        """
        expr = self.primary()
        
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        
        return expr
    
    
    def finish_call(self, callee):
        """
        Parse the arguments for a function call expression.
        """
        arguments = []

        # If there's no closing parenthesis, continue parsing arguments.
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                # Parse and append an argument
                arguments.append(self.expression())
                # Check for additional arguments
                if not self.match(TokenType.COMMA):
                    break

                # If there are more than 255 arguments, raise an error
                if len(arguments) >= 255:
                    self.error(self.peek(), "Cannot have more than 255 arguments.")

        # Ensure the closing parenthesis is consumed after parsing all arguments
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        # Return the function call expression with the callee, closing parenthesis, and arguments
        return Call(callee, paren, arguments)
    
    
    
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
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")  # Ensure closing parenthesisreturn expr
            return expr
        
        # if none above matches, we've an error
        self.error(self.peek(), "Expect expression.")
        return None
        
        
        
    ######################################################
    # Synchronization for error recovery
    ######################################################
    
    def synchronize(self):
        """
        Synchronizes the parser by advancing through tokens until it finds a 
        statement boundary. This is typically used to recover from a parsing 
        error and continue parsing subsequent statements.
        The method advances the parser until it finds a semicolon or a token 
        that indicates the start of a new statement, such as a class, function, 
        variable declaration, or control flow keyword (for, if, while, print, 
        return).
        Returns:
            None
        """
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
        Parses the input and returns a list of statements.
        This method repeatedly calls the `declaration` method to parse
        declarations until the end of the input is reached. The parsed
        declarations are collected into a list and returned.
        Returns:
            list: A list of parsed statements.
        """
        
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

        
        
        
    