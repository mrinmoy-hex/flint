from flint.runtime_error import CustomRunTimeError
import json


class Environment:
    def __init__(self, enclosing=None):
        # dictionary to store variable names and their associated values
        self.values = {}
        self.enclosing = enclosing      # reference to the outer scope (None for global scope)
        
        
    def get(self, name):
        """
        Retrieve the value of a variable from the environment.
        Args:
            name (Token): The token representing the variable name.
        Returns:
            Any: The value of the variable if it exists in the environment.
        Raises:
            CustomRunTimeError: If the variable is not found in the environment.
        """
        
        lexeme = name.lexeme    # extract the variable name from the token
        
        if lexeme in self.values:
            # if the var exists in the current env, return its' value
            return self.values[lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)     # search in enclosing scope
        
        # if not found, raise an error
        raise CustomRunTimeError(name, f"Undefined variable '{lexeme}'.")


    def assign(self, name, value):
        """
        Assigns a value to an existing variable in the environment.

        Args:
            name (str): The name of the variable.
            value (any): The value to assign to the variable.

        Raises:
            RuntimeError: If the variable is not defined in the environment.
        """
        lexeme = name.lexeme
        
        if lexeme in self.values:
            # Variable exists in current environment, reassigned
            self.values[lexeme] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        
        raise CustomRunTimeError(name, f"Undefined variable: '{lexeme}.'")    
    
    
    
        
    def define(self, name, value):
        """
        Defines a new variable in the environment.
        
        Prevents redefinition of variables in the same scope.
        
        Args:
            name (str): The name of the variable.
            value (any): The value associated with the variable.
        
        Raises:
            RuntimeError: If the variable is already defined in the current scope.
    
        """
        key = name.lexeme if hasattr(name, 'lexeme') else name
        if key in self.values:
            raise CustomRunTimeError(name, f"Variable '{key}' already defined in the current scope.")
    
        self.values[key] = value
        
        
    def log_environment(self, filepath):
        try:
            with open(filepath, 'w') as file:
                json.dump(self.values, file, indent=4)
            print(f"Environment state save to: {filepath}.")
        except Exception as e:
            print(f"Error logging environment state: {e}")

