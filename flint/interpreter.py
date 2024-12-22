# Imports
from flint.token_types import TokenType
from flint.runtime_error import CustomRunTimeError
from flint.environment import Environment
from tools.raise_error import *


class Interpreter():
    def __init__(self, environment):
        """
        Initialize the interpreter with the given environment.
        
        Args:
            environment (Environment): The environment to use for variable storage.
        """
        self.environment = environment
    
    
    ############################################
    # Interpreter’s public API
    ############################################
    
    def interpret(self, statements):
        """
        Executes a list of statements sequentially.

        Args:
            statements (List[Stmt]): A list of statements to be executed.

        Handles runtime errors gracefully by reporting them using the runtime_error method.
    """
        try:
            for statement in statements:
                self.execute(statement)     # execute each statement in order
        except CustomRunTimeError as error:
            runtime_error(error)            # handle and report runtime errors
            
            
            
    def execute(self, stmt):
        """
        Executes a statement by delegating to its accept method.

        Args:
            stmt (Stmt): The statement to be executed.
        """
        if stmt is None:
            # saveguard to avoid AttributeError
            return
        
        
        stmt.accept(self)   # Delegate execution to the statement's accept method.
            
            
    def execute_block(self, statements, environment):
        """
        Executes a block of statements in a given environment.
    
        Args:
            statements (list): The statements to execute.
            environment (Environment): The environment for the block's scope.
        """
        previous = self.environment
        try:
            self.environment = environment      # switch to new environment
            
            for statement in statements:
                self.execute(statement)         # execute each statement in the block
        finally:
            self.environment = previous         # restore the previous environment
            
            
            
    
    ############################################
    # Visitor Methods 
    ############################################
    
    def visit_block(self, stmt):
        """
        Visits a block statement, creating a new environment for the block and executing
        the statements within it.

        Args:
            stmt: The block statement to be visited, which contains a list of statements.

        Returns:
            None
        """
        # create a new environment that chains to the current one
        environment = Environment(self.environment)
        self.execute_block(stmt.statements, environment)
        return None
    
    
    
    def visit_literal(self, expr):
        """Evaluates literal expression"""
        return expr.value
    
    
    def visit_grouping(self, expr):
        """Evaluates a grouping expression"""
        return self.evaluate(expr.expression)
    
    
    def evaluate(self, expr):  
        """Evaluates the given expression by accepting the visitor""" 
        return expr.accept(self)
    
    
    
    def visit_expression(self, stmt):
        """
        Executes an expression statement.

        Args:
            stmt: The expression statement to execute.
        """
        self.evaluate(stmt.expression)
        return None
    
    
    def visit_print(self, stmt):
        """
        Evaluates and executes a print statement.

        This method evaluates the given expression in the print statement 
        and outputs the result to the console using Python's built-in print function. 
        A custom print library may replace this in the future for enhanced functionality.

        Args:
            stmt (PrintStmt): The print statement to evaluate.
        """
        value = self.evaluate(stmt.expression)      # evaluate the expression in the statement
        print(self.stringify(value))                # convert the value to a string
        return None
    
    
    def visit_var(self, stmt):
        """
        Evaluates and executes a variable declaration statement.

        This method evaluates the initializer expression in the variable declaration statement 
        and stores the result in the environment with the variable's name.

        Args:
            stmt (VarStmt): The variable declaration statement to execute
        """
        value = None        # default value for the variable
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer) # evaluate the initializer expression
            
        # define the variable in the environment with its value
        self.environment.define(stmt.name, value)
        return None
        
        
    def visit_assign(self, expr):
        """
        Visit an assignment expression, evaluate its value, and assign it to the
        corresponding variable in the environment.

        Args:
            expr: The assignment expression to be visited. It should have 'value'
                and 'name' attributes.

        Returns:
            The evaluated value of the assignment expression.
        """
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
        
        
        
        
    def visit_variable(self, expr):
        """
        Evaluates a variable expression by retrieving its value from the environment.

        Args:
            expr (VariableExpr): The variable expression to evaluate.
        """
        return self.environment.get(expr.name)
    
    
    
        
    def visit_unary(self, expr):
        """Visit unary expression"""
        right = self.evaluate(expr.right)
        
        if expr.operator.type == TokenType.EXCLAMATION:
            return not self.is_truthy(right)
        
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        
        # unreachable
        return None
    
    
    def visit_binary(self, expr):
        """Evaluates binary expressions for supported operators"""
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        
        # handling comparision operator
        if expr.operator.type == TokenType.GREATER_THAN:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        
        elif expr.operator.type == TokenType.GREATER_THAN_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        
        elif expr.operator.type == TokenType.LESS_THAN:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        
        elif expr.operator.type == TokenType.LESS_THAN_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        
        # check for equality operators
        
        elif expr.operator.type == TokenType.EXCLAMATION_EQUAL:
            return not self.is_equal(left, right)
        
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        
        
        # handling arighmetic operators
        
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        
        # handling plus for both adding and for concatinating strings
        elif expr.operator.type == TokenType.PLUS:
            # handle addition of two numbers (float)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) + float(right)
            
            # handle string concatenation
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            
            # Raise error for invalid operands
            raise CustomRunTimeError(expr.operator, "Operands must be two numbers or two strings.")
            
            
        # handling also zero division error    
        elif expr.operator.type == TokenType.FORWARD_SLASH:
            self.check_number_operands(expr.operator, left, right)
            try:
                # try to divide
                return float(left) / float(right)
            except ZeroDivisionError:
                raise CustomRunTimeError(expr.operator, "Division by zero is not allowed.")

        
        elif expr.operator.type == TokenType.ASTERISK:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        
        # unreachable if the expression is valid
        return None
    
    
    
    ###########################################
    # Helper methods
    ###########################################
    
    def is_truthy(self, object):
        """Determines the truthiness of an object based on Flints's semantics"""
        return bool(object) if isinstance(object, bool) else object is not None
    
    
    def is_equal(self, left, right):
        if left is None and right is None:
            return True
        
        if left is None or right is None:
            return False
        
        return left == right
    
    
    def check_number_operand(self, operator, operand):
        """Ensure the operand is a number else raise an error"""
        if isinstance(operand, (int, float)):
            return
        # custom exception
        raise CustomRunTimeError(f"Operand must be a number for operator '{operator.lexeme}'.")
        
        
    def check_number_operands(self, operator, left, right):
        """Ensures that both operands are numbers"""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return  # both operands are numbers, proceed
        
        raise CustomRunTimeError(operator, "Operands must be numbers")
            
            
    def stringify(self, obj):
        """
        Converts the given object to its string representation.
        Args:
            obj: The object to be converted to a string. It can be of any type.
        Returns:
            str: The string representation of the object. If the object is None, 
                    it returns "nil". If the object is a float and ends with ".0", 
                    the ".0" part is removed from the string representation.
        """
        if obj is None:
            return "nil"
        
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]    # removes the ".0" part
            return text
        
        return str(obj)
            