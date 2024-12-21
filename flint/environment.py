from flint.runtime_error import CustomRunTimeError


class Environment:
    def __init__(self):
        # dictionary to store variable names and their associated values
        self.values = {}
        
        
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
        if name in self.values:
            self.values[name] = value
            return
        
        raise CustomRunTimeError(name, f"Undefined variable: '{name.lexeme}.'")    
    
    
    
        
    def define(self, name, value):
        """
        Defines a new variable in the environment.
        
        Args:
            name (str): The name of the variable.
            value (any): The value associated with the variable.
        """
        self.values[name] = value

