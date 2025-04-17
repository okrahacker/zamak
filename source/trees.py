# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from lexer import Token


class Expr:
    def __init__(self):
        self.lineNumber: int = 0
    def __str__(self) -> str:
        return self.__repr__()

class Stmt:
    def __init__(self):
        self.lineNumber: int = 0
    def __str__(self) -> str:
        return self.__repr__()

class LiteralExpr(Expr):
    def __init__(self, literal: Token):
        self.literal: Token = literal
        self.lineNumber: int = literal.lineNumber
    
    def __repr__(self) -> str:
        return f'{self.literal.lexeme}'

class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
        self.lineNumber: int = left.lineNumber
    
    def __repr__(self) -> str:
        return f'({self.left} {self.operator.lexeme} {self.right})'

class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr
        self.lineNumber: int = expr.lineNumber

    def __repr__(self) -> str:
        return f'{self.expr};'
