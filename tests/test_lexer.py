import pytest
import flint.scanner
from flint.token_types import TokenType

def parses_single_character_tokens():
    source = "(){}"
    scanner = flint.scanner.Scanner(source)
    scanner.scan_tokens()

    tokens = scanner.tokens
    assert tokens[0].type == TokenType.LEFT_PAREN
    assert tokens[1].type == TokenType.RIGHT_PAREN
    assert tokens[2].type == TokenType.LEFT_BRACE
    assert tokens[3].type == TokenType.RIGHT_BRACE
    assert tokens[-1].type == TokenType.EOF
