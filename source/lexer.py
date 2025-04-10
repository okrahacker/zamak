# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from common import reportError
from enum import Enum


DIGITS = '1234567890'

class TokenType(Enum):
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    LEFT_PAREN = 5
    RIGHT_PAREN = 6

    NUMBER = 7


class Token:
    def __init__(self, lineNumber: int, category: TokenType, lexeme: str = ''):
        self.lineNumber: int = lineNumber
        self.category: TokenType = category
        self.lexeme: str = lexeme


class Lexer:
    def __init__(self):
        self.characterIndex: int = 0
        self.sourceCode: str = ''
        self.lineNumber: int = 1
    
    def isAtEnd(self) -> bool:
        return self.characterIndex >= len(self.sourceCode)

    def peek(self) -> str:
        return self.sourceCode[self.characterIndex]
    
    def advance(self) -> str:
        self.characterIndex += 1
        return self.sourceCode[self.characterIndex - 1]
    
    def makeToken(self) -> Token | None:
        character: str = self.advance()
        match character:
            # White space
            case ' ':
                return
            # Comments
            case '/' if self.peek() == '/':
                while not self.isAtEnd() and not self.peek() == '\n':
                    self.advance()
                return
            # New line
            case '\n':
                self.lineNumber += 1
                return
            # Tabs
            case '\t':
                reportError(self.lineNumber, 'Tabs are not allowed.')
            # Single character tokens
            case '+':
                return Token(self.lineNumber, TokenType.PLUS)
            case '-':
                return Token(self.lineNumber, TokenType.MINUS)
            case '*':
                return Token(self.lineNumber, TokenType.STAR)
            case '/':
                return Token(self.lineNumber, TokenType.SLASH)
            case '(':
                return Token(self.lineNumber, TokenType.LEFT_PAREN)
            case ')':
                return Token(self.lineNumber, TokenType.RIGHT_PAREN)
            case _:
                # Fallthrough to the code below.
                pass
        if character in DIGITS:
            numberLexeme: str = character
            while not self.isAtEnd() and (self.peek() in DIGITS or self.peek() in '_'):
                numberLexeme += self.advance()
            return Token(self.lineNumber, TokenType.NUMBER, numberLexeme)
        else:
            reportError(self.lineNumber, f'Unexpected character "{character}".')
    
    def run(self, sourceCode: str) -> list[Token]:
        self.sourceCode = sourceCode
        tokens: list[Token] = []
        while not self.isAtEnd():
            token: Token | None = self.makeToken()
            if token is not None:
                tokens.append(token)
        return tokens
