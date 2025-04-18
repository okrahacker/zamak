# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from enum import Enum
from common import reportError
from trees import *


class DataType(Enum):
    INTEGER = 0
    BOOLEAN = 1
    STRING = 2
    FLOAT = 3


class TypeChecker:
    def checkExpr(self, expr: Expr) -> DataType:
        if isinstance(expr, LiteralExpr):
            if expr.literal.category == TokenType.INTEGER_LIT:
                return DataType.INTEGER
            elif expr.literal.category == TokenType.FLOAT_LIT:
                return DataType.FLOAT
            elif expr.literal.category == TokenType.BOOLEAN_LIT:
                return DataType.BOOLEAN
            elif expr.literal.category == TokenType.STRING_LIT:
                return DataType.STRING
            else:
                raise NotImplementedError
        elif isinstance(expr, UnaryExpr):
            if expr.operator.category in [TokenType.MINUS]:
                exprType: DataType = self.checkExpr(expr.expr)
                if exprType not in [DataType.INTEGER, DataType.FLOAT]:
                    reportError(expr.lineNumber,
                                f'Invalid type for "{expr.operator.lexeme}".')
                return exprType
            elif expr.operator.lexeme == 'not':
                exprType: DataType = self.checkExpr(expr.expr)
                if exprType not in [DataType.BOOLEAN]:
                    reportError(expr.lineNumber,
                                f'Invalid type for "{expr.operator.lexeme}".')
                return exprType
            else:
                raise NotImplementedError
        elif isinstance(expr, BinaryExpr):
            leftType: DataType = self.checkExpr(expr.left)
            rightType: DataType = self.checkExpr(expr.right)
            if rightType != leftType:
                reportError(expr.lineNumber,
                            f'Types for "{expr.operator.lexeme}" don\'t match.')
            operatorType: TokenType = expr.operator.category
            if operatorType in [TokenType.MINUS, TokenType.STAR,
                                TokenType.SLASH, TokenType.PERCENT]:
                if leftType not in [DataType.INTEGER, DataType.FLOAT]:
                    reportError(expr.lineNumber,
                                f'Invalid types for "{expr.operator.lexeme}".')
                return leftType
            elif operatorType in [TokenType.PLUS]:
                if leftType not in [DataType.INTEGER, DataType.FLOAT, DataType.STRING]:
                    reportError(expr.lineNumber,
                                f'Invalid types for "{expr.operator.lexeme}".')
                return leftType
            elif operatorType in [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL,
                                  TokenType.GREATER_EQUAL, TokenType.LESSER_EQUAL]:
                return DataType.BOOLEAN
            elif operatorType in [TokenType.GREATER, TokenType.LESSER]:
                if leftType not in [DataType.INTEGER, DataType.FLOAT]:
                    reportError(expr.lineNumber,
                                f'Invalid types for "{expr.operator.lexeme}".')
                return DataType.BOOLEAN 
            elif expr.operator.lexeme in ['and', 'or']:
                if leftType not in [DataType.BOOLEAN]:
                    reportError(expr.lineNumber,
                                f'Invalid types for "{expr.operator.lexeme}".')
                return DataType.BOOLEAN
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
            
    def checkStmt(self, stmt: Stmt):
        if isinstance(stmt, ExprStmt):
            self.checkExpr(stmt.expr)
        else:
            raise NotImplementedError

    def run(self, trees: list[Stmt]):
        for stmt in trees:
            self.checkStmt(stmt)