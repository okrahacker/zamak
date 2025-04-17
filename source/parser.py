# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from common import reportError
from lexer import Token, TokenType
from trees import *


class Parser:
    def __init__(self):
        self.tokenIndex: int = 0
        self.tokens: list[Token] = []
    
    def isAtEnd(self) -> bool:
        return self.tokenIndex >= len(self.tokens)

    def peekBehind(self) -> Token:
        return self.tokens[self.tokenIndex - 1]

    def peek(self) -> Token:
        return self.tokens[self.tokenIndex]
    
    def advance(self) -> Token:
        self.tokenIndex += 1
        return self.tokens[self.tokenIndex - 1]
    
    def match(self, *tokenTypes: TokenType) -> bool:
        for tokenType in tokenTypes:
            if self.isAtEnd():
                return False
            elif self.peek().category == tokenType:
                return True
        return False
    
    def matchKeyword(self, *keywords: str) -> bool:
        for keyword in keywords:
            if self.isAtEnd():
                return False
            elif self.match(TokenType.KEYWORD) and self.peek().lexeme == keyword:
                return True
        return False
    
    def expect(self, tokenType: TokenType, errorMessage: str):
        if not self.match(tokenType):
            if self.isAtEnd():
                reportError(self.peekBehind().lineNumber, errorMessage)
            reportError(self.peek().lineNumber, errorMessage)
        else:
            self.advance()
    
    def parse(self) -> Stmt:
        return self.exprStmt()
    
    def exprStmt(self) -> Stmt:
        stmt: Stmt = ExprStmt(self.expr())
        self.expect(TokenType.SEMICOLON, 'Expected a ";" after expression statement.')
        return stmt
    
    def expr(self) -> Expr:
        return self.logicalExpr()
    
    def logicalExpr(self) -> Expr:
        left: Expr = self.comparisonExpr()
        while self.matchKeyword('and', 'or'):
            operator: Token = self.advance()
            right: Expr = self.comparisonExpr()
            left = BinaryExpr(left, operator, right)
        return left

    def comparisonExpr(self) -> Expr:
        left: Expr = self.termExpr()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL,
                         TokenType.LESSER, TokenType.LESSER_EQUAL,
                         TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator: Token = self.advance()
            right: Expr = self.termExpr()
            left = BinaryExpr(left, operator, right)
        return left

    def termExpr(self) -> Expr:
        left: Expr = self.factorExpr()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator: Token = self.advance()
            right: Expr = self.factorExpr()
            left = BinaryExpr(left, operator, right)
        return left
    
    def factorExpr(self) -> Expr:
        left: Expr = self.unaryExpr()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator: Token = self.advance()
            right: Expr = self.unaryExpr()
            left = BinaryExpr(left, operator, right)
        return left
    
    def unaryExpr(self) -> Expr:
        if self.peek().lexeme == 'not' or self.match(TokenType.MINUS):
            operator: Token = self.advance()
            expr: Expr = self.unaryExpr()
            return UnaryExpr(operator, expr)
        else:
            return self.primaryExpr()
    
    def primaryExpr(self) -> Expr:
        if self.isAtEnd():
            reportError(self.peekBehind().lineNumber,
                        'Expected an expression before the end of the file.')
        elif self.match(TokenType.LEFT_PAREN):
            self.advance()  # Consume the '('.
            expr: Expr = self.expr()
            self.expect(TokenType.RIGHT_PAREN, 'Expected a closing ")".')
            return expr
        elif self.match(TokenType.INTEGER_LIT, TokenType.BOOLEAN_LIT,
                        TokenType.STRING_LIT, TokenType.ARRAY_LIT,
                        TokenType.STRUCT_LIT, TokenType.FLOAT_LIT):
            return LiteralExpr(self.advance())
        else:
            reportError(self.peek().lineNumber, 'Expected an expression.')
        return Expr()


    def run(self, tokens: list[Token]) -> list[Stmt]:
        self.tokens = tokens
        trees: list[Stmt] = []
        while not self.isAtEnd():
            trees.append(self.parse())
        return trees