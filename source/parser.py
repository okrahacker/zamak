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
    
    def expect(self, tokenType: TokenType, errorMessage: str):
        if not self.match(tokenType):
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
        return self.termExpr()
    
    def termExpr(self) -> Expr:
        left: Expr = self.factorExpr()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator: Token = self.advance()
            right: Expr = self.factorExpr()
            left = BinaryExpr(left, operator, right)
        return left
    
    def factorExpr(self) -> Expr:
        left: Expr = self.primaryExpr()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator: Token = self.advance()
            right: Expr = self.primaryExpr()
            left = BinaryExpr(left, operator, right)
        return left
    
    def primaryExpr(self) -> Expr:
        if self.match(TokenType.LEFT_PAREN):
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