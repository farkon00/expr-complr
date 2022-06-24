from lexer.lexer import Lexer
from lexer.token import Token

def print_tokens(tokens : list[Token]):
    for token in tokens:
        print(f"{token.index} {token.type.name} {token.value}")

def main():
    lexer = Lexer(input("Expression: "))
    print_tokens(lexer.lex())

if __name__ == "__main__":
    main()