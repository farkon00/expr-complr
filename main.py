from subprocess import run
from lexer.lexer import Lexer
from lexer.token import Token
from parser.expr import *

from parser.parser import Parser

from compiler.compiler import Compiler

# Availiable modes
# Mostly for debugging
# LEXER - output tokens
# PARSER - output expression tree
# COMPILER - output compiled asm
# <blank> - regular mode
OUTPUT_MODE = ""

def print_tokens(tokens : list[Token]):
    for token in tokens:
        print(f"{token.index} {token.type.name} {token.value}")

def execute_expr(expr : str):
    try:
        lexer = Lexer(expr)
        tokens = lexer.lex()
        parser = Parser(tokens, lexer.text)
        expr = parser.parse_expr()
        if expr is None:
            expr = Expr(ExprType.INTEGER, value=0)
        compiler = Compiler(expr)
    except SystemExit:
        return

    with open("output.asm", "w") as f:
        f.write(compiler.compile())
    run(["fasm", "output.asm"], capture_output=True)

    with open("output_result", "wb") as out:
        run(["./output"], stdout=out)

    with open("output_result", "rb") as out:
        print(int.from_bytes(out.read(), "little"))

def main():
    if not OUTPUT_MODE:
        print("Use \"exit\" to exit")
        while True:
            inp = input(" > ")
            if inp.strip() == "exit":
                exit(0)
            execute_expr(inp)

    lexer = Lexer(input("Expression: "))
    tokens = lexer.lex()
    parser = Parser(tokens, lexer.text)
    expr = parser.parse_expr()
    compiler = Compiler(expr)
    
    if OUTPUT_MODE == "LEXER":
        print_tokens(tokens)
        return
    if OUTPUT_MODE == "PARSER":
        print(expr)
        return
    if OUTPUT_MODE == "COMPILER":
        print(compiler.compile())
        return

    print(f"Unknown output mode: {OUTPUT_MODE}") 
    print("Put blank in OUTPUT_MODE to run at regular mode")

if __name__ == "__main__":
    main()