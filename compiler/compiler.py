from error import throw_error
from parser.expr import *

class Compiler:
    OPER_ASM = {
        ExprType.ADD : "pop rax\npop rbx\nadd rax, rbx\npush rax\n",
        ExprType.SUB : "pop rax\npop rbx\nsub rax, rbx\npush rax\n",
        ExprType.MUL : "pop rax\npop rbx\nimul rbx\npush rax\n",
        ExprType.DIV : "pop rax\npop rbx\nmov rdx, 0\nidiv rbx\npush rax\n",
        ExprType.MOD : "pop rax\npop rbx\nmov rdx, 0\nidiv rbx\npush rdx\n",
        ExprType.POW : "pop rax\npop rbx\ncall power\npush rax\n",
    }

    def __init__(self, expr: Expr):
        self.expr = expr
        self.asm = ""
        self.chained = False
        self.prev_result = None

    def reload(self, expr: Expr, text: str):
        self.expr = expr
        self.asm = ""
        self.text = text
        self.chained = False

    def generate_fasm_header(self):
        self.asm += \
        """
        format ELF64 executable 3

        segment readable executable
            power:
                mov rcx, rax
                .L0:
                    mul rcx
                    sub rbx, 1
                    cmp rbx, 1
                    jnz .L0
                ret

            entry start
            start:
        """

    def generate_fasm_footer(self):
        self.asm += \
        """
            pop rax
            mov [result], rax

            mov rax, 1
            mov rdi, 1
            mov rsi, result
            mov rdx, 8
            syscall

            mov rax, 60
            mov rdi, 0
            syscall

            segment readable writable
            result: rb 8
        """

    def compile(self, expr: Expr = None):
        main = expr is None
        if main:
            expr = self.expr
            self.generate_fasm_header()
        if expr.type == ExprType.INTEGER:
            self.asm += f"mov rax, {expr.value}\npush rax\n"
        elif expr.type in self.OPER_ASM:
            self.compile(expr.right)
            self.compile(expr.left)
            self.asm += self.OPER_ASM[expr.type]
        elif expr.type == ExprType.CHAIN:
            if self.prev_result is None or self.chained:
                throw_error("Missing left operand", index=expr.token.index, line=self.text)
            else:
                self.chained = True
                self.asm += f"mov rax, {self.prev_result}\npush rax\n"

        if main:
            self.generate_fasm_footer()
            return self.asm