#################
# Error handling for Lox
#################
import sys
from lox.token_types import TokenType


def error(line: int, message: str) -> None:
    """Reports an error at a specific line."""
    report(line, "", message)
    



def report(line: int, pos_where: str, message: str):
    """Formats and reports an error message."""
    print(f"[line {line}] Error{pos_where}: {message}", file=sys.stderr)
    had_error = True