# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from common import reportError
from typechecker import DataType, BUILT_IN_TYPES
from trees import *


class NameResolver:
    def __init__(self):
        self.declaredIdentifiers: dict[str, DataType] = {}

    def declare(self, identifier: Token, dataType: DataType):
        if identifier.lexeme in self.declaredIdentifiers:
            reportError(identifier.lineNumber,
                        f'Identifier "{identifier.lexeme}" has already been declared.')
        self.declaredIdentifiers[identifier.lexeme] = dataType

    def resolveExpr(self, expr: Expr):
        if isinstance(expr, IdentifierExpr):
            if expr.identifier.lexeme not in self.declaredIdentifiers:
                reportError(expr.lineNumber, f'Identifier "{expr.identifier.lexeme}"'
                                              ' hasn\'t been declared yet.')
        elif isinstance(expr, LiteralExpr):
            pass
        elif isinstance(expr, UnaryExpr):
            self.resolveExpr(expr.expr)
        elif isinstance(expr, BinaryExpr):
            self.resolveExpr(expr.left)
            self.resolveExpr(expr.right)
        else:
            raise NotImplementedError

    def resolveStmt(self, stmt: Stmt):
        if isinstance(stmt, LetStmt):
            if not isinstance(stmt.typeExpr, IdentifierExpr):
                raise NotImplementedError
            if stmt.typeExpr.identifier.lexeme in BUILT_IN_TYPES:
                self.declare(stmt.identifier,
                             BUILT_IN_TYPES[stmt.typeExpr.identifier.lexeme])
            else:
                reportError(stmt.lineNumber,
                            f'Identifier "{stmt.typeExpr.identifier.lexeme}"'
                             ' has\'t been declared yet.')
        elif isinstance(stmt, AssignStmt):
            self.resolveExpr(stmt.identifier)
            self.resolveExpr(stmt.expr)
        elif isinstance(stmt, ExprStmt):
            self.resolveExpr(stmt.expr)
        else:
            raise NotImplementedError

    def run(self, trees: list[Stmt]) -> dict[str, DataType]:
        for tree in trees:
            self.resolveStmt(tree)
        return self.declaredIdentifiers