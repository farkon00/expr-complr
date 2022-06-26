import cmd
import os
import sys

from subprocess import run
from interpreter.interpreter import Interpreter

from lexer.lexer import Lexer
from lexer.token import Token
from parser.expr import *

from parser.parser import Parser

from compiler.compiler import Compiler

class REPL(cmd.Cmd):
    mode = "i"
    intro = "Use \"exit\" to exit"
    prompt = " > "

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.mode == "i":
            self.inter = Interpreter()
            print("Running in interpreted mode")
        elif self.mode == "c":
            self.compl = Compiler(None)
            print("Running in compiled mode")

    def _execute(self, expr: Expr, line: str):
        if self.mode == "i":
            try:
                res = self.inter.compute(expr, line)
            except SystemExit:
                self.inter.reload(None)
                raise SystemExit
            print(res)
            self.inter.reload(res)

        elif self.mode == "c":
            self.compl.reload(expr, line)
            with open("output.asm", "w") as f:
                f.write(self.compl.compile())
            run(["fasm", "output.asm"], capture_output=True)

            with open("output_result", "wb") as out:
                run(["./output"], stdout=out)

            with open("output_result", "rb") as out:
                result = int.from_bytes(out.read(), "little")
                print(result if result < NEGATIVE_BOUNDRY else result - (NEGATIVE_BOUNDRY * 2 + 2))
                self.compl.prev_result = result

            os.remove("output.asm")
            os.remove("output_result")
            os.remove("output")
        else:
            assert False, "Unknown mode"

    def onecmd(self, expr):
        line = expr
        if expr.strip() == "exit":
            return True
        try:
            lexer = Lexer(expr)
            tokens = lexer.lex()
            parser = Parser(tokens, lexer.text)
            expr = parser.parse_expr()
            if expr is None:
                expr = Expr(ExprType.INTEGER, value=0)
            self._execute(expr, line)
        except SystemExit:
            pass

        return False

# Availiable modes
# Mostly for debugging
# LEXER - output tokens
# PARSER - output expression tree
# COMPILER - output compiled asm
# <blank> - regular mode
OUTPUT_MODE = ""

NEGATIVE_BOUNDRY = 9_223_372_036_854_775_807

def print_tokens(tokens : list[Token]):
    for token in tokens:
        print(f"{token.index} {token.type.name} {token.value}")

def main():
    if not OUTPUT_MODE:
        if len(sys.argv) < 2:
            REPL.mode = "i"
        elif sys.argv[1] == "com" or sys.argv[1] == "c":
            REPL.mode = "c"
        REPL().cmdloop()
        exit(0)

    lexer = Lexer(input("Expression: "))
    tokens = lexer.lex()
    
    if OUTPUT_MODE == "LEXER":
        print_tokens(tokens)
        return
    if OUTPUT_MODE == "PARSER":
        parser = Parser(tokens, lexer.text)
        expr = parser.parse_expr()
        print(expr)
        return
    if OUTPUT_MODE == "COMPILER":
        parser = Parser(tokens, lexer.text)
        expr = parser.parse_expr()
        compiler = Compiler(expr)
        print(compiler.compile())
        return

    print(f"Unknown output mode: {OUTPUT_MODE}") 
    print("Put blank in OUTPUT_MODE to run at regular mode")

if __name__ == "__main__":
    main()