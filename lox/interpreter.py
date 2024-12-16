from lox.ast.expr import ExprVisitor
from lox.token_types import TokenType
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
            if isinstance(right, (int, float)):
                return -float(right)
        
        
        
        # unreachable
        return None
    
    
    def visit_binary(self, expr):
        """Evaluates binary expressions for supported operators"""
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        
        # handling comparision operator
        if expr.operator.type == TokenType.GREATER_THAN:
            return float(left) > float(right)
        
        elif expr.operator.type == TokenType.GREATER_THAN_EQUAL:
            return float(left) >= float(right)
        
        elif expr.operator.type == TokenType.LESS_THAN:
            return float(left) < float(right)
        
        elif expr.operator.type == TokenType.LESS_THAN_EQUAL:
            return float(left) <= float(right)
        
        # check for equality operators
        
        elif expr.operator.type == TokenType.EXCLAMATION_EQUAL:
            return not self.is_equal(left, right)
        
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        
        
        # handling arighmetic operators
        
        elif expr.operator.type == TokenType.MINUS:
            return float(left) - float(right)
        
        # handling plus for both adding and for concatinating strings
        elif expr.operator.type == TokenType.PLUS:
            # handle addition of two numbers (float)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) + float(right)
            
            # handle string concatenation
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            
            # handling the edge cases like cannot concatenate string with number like that....in future :D
            
            
        elif expr.operator.type == TokenType.FORWARD_SLASH:
            return float(left) / float(right)
        
        elif expr.operator.type == TokenType.ASTERISK:
            return float(left) * float(right)
        
        # unreachable if the expression is valid
        return None
    
    
        
        
        
    
    
    
    ###########################################
    # Helper method
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
        
        
