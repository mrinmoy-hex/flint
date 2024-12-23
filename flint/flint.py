#############################################
# Imports
#############################################

import sys
from tools.raise_error import *
from flint.scanner import Scanner
from flint.parser import Parser
from flint.interpreter import Interpreter
from flint.environment import Environment   

class Flint:

    had_error = False
    had_runtime_error = False
    global_environment = Environment()      # shared environment for REPL

    @staticmethod
    def main() -> None:
        """
        The main entry point for the Flint application.

        This function handles the command-line arguments and determines whether to
        run a script file or enter REPL (Read-Eval-Print Loop) mode.

        Usage:
            Flint [script]

        If a script file is provided as an argument, it runs the script.
        If no arguments are provided, it starts the REPL mode.

        Exits with status code 64 if more than one argument is provided.
        """
        if len(sys.argv) > 2:
            print("Usage: Flint [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Flint.run_file(sys.argv[1])
        else:
            # for REPL mode
            Flint.run_prompt()


    @staticmethod
    def run_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                Flint.run(content, Flint.global_environment)
                
            # Log the environment state after running the file
            # Flint.global_environment.log_environment("debug/environment_state.json")



        except IOError as e:
            print(f"Error reading file: {e}")
            exit(64)    # std exit code for file-related erros

        # indicate an error in the exit code
        if Flint.had_error:
            sys.exit(64)
        
        if Flint.had_runtime_error:
            sys.exit(70)



    @staticmethod
    def run_prompt():
        """
        Starts a Read-Eval-Print Loop (REPL) for the Flint programming language.

        This function continuously prompts the user for input, evaluates the input
        using the Flint interpreter, and prints the result. The loop terminates
        when the user inputs an empty string or 'exit'.

        Usage:
            run_prompt()
        Note:
            This function sets `Flint.had_error` to False after each command execution.
        """
        print("Flint REPL (type 'exit' to quit)")
        while True:
            line = input(">>> ")
            if line == "" or line == "exit":
                break
            Flint.run(line, Flint.global_environment, is_repl_mode=True)
            Flint.had_error = False


    @staticmethod
    def run(source, environment, is_repl_mode=False):
        """
        Compiles and executes the given source code.
        """
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, is_repl_mode=is_repl_mode)
    
        statements = parser.parse()
    
        # Stop further processing if there were syntax errors
        if statements is None or had_error:
            return
    
        interpreter = Interpreter(environment)  # use shared environment
    
        # Try to interpret the valid expression
        try:
            interpreter.interpret(statements)
        except RuntimeError as runtime_err:
            from tools.raise_error import runtime_error
            runtime_error(runtime_err)
            
        # After execution, log the environment state
        # environment.log_environment("debug/environment_state.json")


if __name__ == '__main__':
    Flint.main()