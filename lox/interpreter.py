# Imports
from lox.token_types import TokenType
from lox.runtime_error import CustomRunTimeError
from tools.raise_error import *


class Interpreter:
    
    def visit_literal(self, expr):
        """Evaluates literal expression"""
        return expr.value
    
    
    def visit_grouping(self, expr):
        """Evaluates a grouping expression"""
        return self.evaluate(expr.expression)
    
    
    def evaluate(self, expr):  
        """Evaluates the given expression by accepting the visitor""" 
        return expr.accept(self)
        
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
            
            
            
        elif expr.operator.type == TokenType.FORWARD_SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        
        elif expr.operator.type == TokenType.ASTERISK:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        
        # unreachable if the expression is valid
        return None
    
    
    
    ###########################################
    # Helper methods
    ###########################################
    
    def is_truthy(self, object):
        """Determines the truthiness of an object based on Lox's semantics"""
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
        if obj is None:
            return "nil"
        
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]    # removes the ".0" part
            return text
        
        return str(obj)
            
            
    ############################################
    # Interpreter’s public API
    ############################################
    
    def interpret(self, expression):
        """
        Interprets the expression, evaluates it, and prints the result.
    
        Handles exceptions by printing runtime errors with their respective line number.
        """
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except CustomRunTimeError as error:
            runtime_error(error)
    
    
    
            
