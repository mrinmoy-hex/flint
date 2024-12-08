import pytest
import lox.scanner
from lox.token_types import TokenType

def parses_single_character_tokens():
    source = "(){}"
    scanner = lox.scanner.Scanner(source)
    scanner.scan_tokens()

    tokens = scanner.tokens
    assert tokens[0].type == TokenType.LEFT_PAREN
    assert tokens[1].type == TokenType.RIGHT_PAREN
    assert tokens[2].type == TokenType.LEFT_BRACE
    assert tokens[3].type == TokenType.RIGHT_BRACE
    assert tokens[-1].type == TokenType.EOF
