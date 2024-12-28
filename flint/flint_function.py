from flint.environment import Environment
from flint.flint_callable import FlintCallable

class FlintFunction(FlintCallable):
    
    def __init__(self, declaration):
        """
        Represents a function in Flint.
        """
        self.declaration = declaration
        
    
    def call(self,interpreter, arguments):
        """
        Calls the function with the given arguments.
        """
        environment = Environment(interpreter.globals)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])
            
        interpreter.execute_block(self.declaration.body, environment)
        return None
    
    
    def arity(self):
        """
        Returns the number of parameters the function takes.
        """
        return len(self.declaration.params)
    
    
    def to_string(self):
        """
        Returns the string representation of the function.
        """
        return f"<fn {self.declaration.name.lexeme}>"