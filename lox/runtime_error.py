
class CustomRunTimeError(Exception):
    """Custom exception for runtime errors with a token context"""
    
    def __init__(self, tokens, message):
        super().__init__(message)   # initialize the base class with the new message
        self.token = tokens        # store the tokens associated with the error
        self.message = message