from flint.runtime_error import CustomRunTimeError


class Environment:
    def __init__(self):
        # dictionary to store variable names and their associated values
        self.values = {}
        
        
    def get(self, name):
        """Retrives the value of a variable by its name"""
        lexeme = name.lexeme    # extract the variable name from the token
        
        if lexeme in self.values:
            # if the var exists in the current env, return its' value
            return self.values[lexeme]
        
        # if not found, raise an error
        raise CustomRunTimeError(name, f"Undefined variable '{lexeme}'.")

        
    def define(self, name, value):
        """
        Defines a new variable in the environment.
        
        Args:
            name (str): The name of the variable.
            value (any): The value associated with the variable.
        """
        self.values[name] = value

