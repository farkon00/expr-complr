from lexer.lexer import Lexer
from lexer.token import Token

from parser.parser import Parser

# Availiable modes
# LEXER - output tokens
# PARSER - output expression tree
OUTPUT_MODE = "PARSER"

def print_tokens(tokens : list[Token]):
    for token in tokens:
        print(f"{token.index} {token.type.name} {token.value}")

def main():
    lexer = Lexer(input("Expression: "))
    tokens = lexer.lex()
    if OUTPUT_MODE == "LEXER":
        print_tokens(tokens)
        return
    if OUTPUT_MODE == "PARSER":
        parser = Parser(tokens, lexer.text)
        print(parser.parse_expr())
        return

    # TODO: when project will have minimal functionality, add:
    # Put blank in output mode to run at regular mode
    print(f"Unknown output mode: {OUTPUT_MODE}") 

if __name__ == "__main__":
    main()