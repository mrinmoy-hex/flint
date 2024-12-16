#############################################
# Imports
#############################################

import sys
from tools.raise_error import *
from lox.scanner import Scanner
from lox.parser import Parser
from tools.ast_printer import AstPrinter
from lox.interpreter import Interpreter

class Lox:

    had_error = False
    had_runtime_error = False

    @staticmethod
    def main() -> None:
        if len(sys.argv) > 2:
            print("Usage: lox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            # for REPL mode
            Lox.run_prompt()


    @staticmethod
    def run_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                Lox.run(content)


        except IOError as e:
            print(f"Error reading file: {e}")
            exit(64)    # std exit code i found

        # indicate an error in the exit code
        if Lox.had_error:
            sys.exit(64)
        
        if Lox.had_runtime_error:
            sys.exit(70)



    @staticmethod
    def run_prompt():
        print("LOX REPL (type 'exit' to quit)")
        while True:
            line = input("> ")
            if line == "" or line == "exit":
                break
            Lox.run(line)
            Lox.had_error = False


    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        
        interpreter = Interpreter()
        
        expression = parser.parse()
        if expression is None:
            raise ValueError("Parsing failed. Expression is None.")
        
        # stop if there was a syntax error
        if had_error:
            return
        
        interpreter.interpret(expression)

        # print the AST
        # print(AstPrinter().print_ast(expression))


if __name__ == '__main__':
    Lox.main()