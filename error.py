import sys


def throw_error(message: str, index: int = 0, line: str = "", lexer=None):
    if lexer is not None:
        line = lexer.text
        index = lexer.index
    
    sys.stderr.write(f"\033[31;1mError\033[0m: {message}\n")
    sys.stderr.write("\t" + line + "\n")
    sys.stderr.write("\t" + " " * index + "^\n")

    exit(1)