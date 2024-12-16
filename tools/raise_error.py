#################
# Error handling for Lox
#################
import sys
from lox.token_types import TokenType
from lox.token import *

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
    
    
def runtime_error(error):
    """Handles runtime errors by printing the error message."""
    print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
    had_runtime_error = True
    

