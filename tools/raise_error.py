#################
# Error handling for Flint
#################
import sys
from flint.token_types import TokenType
from flint.token import *
from flint.runtime_error import CustomRunTimeError

had_error = False   # to track if an error occured

def error(token: Token, message: str) -> None:
    """Reports an error at a specific token."""
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)
    


def report(line: int, pos_where: str, message: str):
    """Formats and reports an error message."""
    
    global had_error 
    print(f"[line {line}] Error{pos_where}: {message}", file=sys.stderr)
    had_error = True
    
    
def runtime_error(error: CustomRunTimeError) -> None:
    """Handles runtime errors by printing the error message."""
    global had_error
    print(f"[line {error.token.line}] {error.message}\n", file=sys.stderr)
    had_error = True
    

