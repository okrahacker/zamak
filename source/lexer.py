# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from common import reportError
from enum import Enum


DIGITS = '1234567890'
ALPHAS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
KEYWORDS = ['and', 'not', 'or', 'let', 'set']
INDENT_AMOUNT = 4


class TokenType(Enum):
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    LEFT_PAREN = 5
    RIGHT_PAREN = 6
    SEMICOLON = 7
    EQUAL = 8
    EQUAL_EQUAL = 9
    GREATER = 10
    GREATER_EQUAL = 11
    LESSER = 12
    LESSER_EQUAL = 13
    BANG_EQUAL = 14
    DOT = 15
    COMMA = 16
    PERCENT = 17
    LEFT_CURLY = 18
    RIGHT_CURLY = 19

    KEYWORD = 20
    IDENTIFIER = 21

    INDENT = 22
    DEDENT = 23

    INTEGER_LIT = 100
    BOOLEAN_LIT = 101
    STRING_LIT = 102
    ARRAY_LIT = 103
    STRUCT_LIT = 104
    FLOAT_LIT = 105


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
        self.indentLevel: int = 0
    
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
                if self.peek() == ' ':
                    spaces: int = 0
                    while not self.isAtEnd() and self.peek() == ' ':
                        spaces += 1
                        self.advance()
                    if spaces % INDENT_AMOUNT != 0:
                        reportError(self.lineNumber, f'Indent must be a multiple of {INDENT_AMOUNT}.')
                    if spaces > self.indentLevel * INDENT_AMOUNT:
                        self.indentLevel += 1
                        return Token(self.lineNumber, TokenType.INDENT,)
                    elif spaces < self.indentLevel * INDENT_AMOUNT:
                        self.indentLevel -= 1
                        return Token(self.lineNumber, TokenType.DEDENT)
                return
            # Tabs
            case '\t':
                reportError(self.lineNumber, 'Tabs are not allowed.')
            # Single character tokens
            case '+':
                return Token(self.lineNumber, TokenType.PLUS, '+')
            case '-':
                return Token(self.lineNumber, TokenType.MINUS, '-')
            case '*':
                return Token(self.lineNumber, TokenType.STAR, '*')
            case '/':
                return Token(self.lineNumber, TokenType.SLASH, '/')
            case '(':
                return Token(self.lineNumber, TokenType.LEFT_PAREN, '(')
            case ')':
                return Token(self.lineNumber, TokenType.RIGHT_PAREN, ')')
            case ';':
                return Token(self.lineNumber, TokenType.SEMICOLON, ';')
            case '.':
                return Token(self.lineNumber, TokenType.DOT, '.')
            case ',':
                return Token(self.lineNumber, TokenType.COMMA, ',')
            case '%':
                return Token(self.lineNumber, TokenType.PERCENT, '%')
            case '{':
                return Token(self.lineNumber, TokenType.LEFT_CURLY, '{')
            case '}':
                return Token(self.lineNumber, TokenType.RIGHT_CURLY, '}')
            # Multiple character tokens
            case '=':
                if self.peek() == '=':
                    self.advance()
                    return Token(self.lineNumber, TokenType.EQUAL_EQUAL, '==')
                return Token(self.lineNumber, TokenType.EQUAL)
            case '>':
                if self.peek() == '=':
                    self.advance()
                    return Token(self.lineNumber, TokenType.GREATER_EQUAL, '>=')
                return Token(self.lineNumber, TokenType.GREATER)
            case '<':
                if self.peek() == '=':
                    self.advance()
                    return Token(self.lineNumber, TokenType.LESSER_EQUAL, '<=')
                return Token(self.lineNumber, TokenType.LESSER)
            case '!' if self.peek() == '=':
                self.advance()
                return Token(self.lineNumber, TokenType.BANG_EQUAL, '!=')
            # String literal
            case "'":
                stringLexeme: str = ''
                while not self.isAtEnd() and self.peek() != "'":
                    stringLexeme += self.advance()
                if self.isAtEnd():
                    reportError(self.lineNumber, 'Expected a quote to close string literal.')
                self.advance()  # Consume the closing "'".
                return Token(self.lineNumber, TokenType.STRING_LIT, stringLexeme)
            case _:
                # Fallthrough to the code below.
                pass
        if character in DIGITS:
            numberLexeme: str = character
            foundDecimalPoint: bool = False
            while not self.isAtEnd() and (self.peek() in DIGITS or self.peek() in ['_', '.']):
                if self.peek() == '.' and not foundDecimalPoint:
                    foundDecimalPoint = True
                elif self.peek() == '.' and foundDecimalPoint:
                    reportError(self.lineNumber, 'More than 1 decimal point in float literal.')
                numberLexeme += self.advance()
            if numberLexeme[len(numberLexeme) - 1] == '.':
                reportError(self.lineNumber, 'Trailing decimal point in float literal.')
            if foundDecimalPoint:
                return Token(self.lineNumber, TokenType.FLOAT_LIT, numberLexeme)
            return Token(self.lineNumber, TokenType.INTEGER_LIT, numberLexeme)
        elif character in ALPHAS:
            lexeme: str = character
            while not self.isAtEnd() and (self.peek() in ALPHAS or self.peek() in DIGITS):
                lexeme += self.advance()
            if lexeme in KEYWORDS:
                return Token(self.lineNumber, TokenType.KEYWORD, lexeme)
            elif lexeme in ['true', 'false']:
                return Token(self.lineNumber, TokenType.BOOLEAN_LIT, lexeme)
            else:
                return Token(self.lineNumber, TokenType.IDENTIFIER, lexeme)
        else:
            reportError(self.lineNumber, f'Unexpected character "{character}".')
    
    def run(self, sourceCode: str) -> list[Token]:
        self.sourceCode = sourceCode
        tokens: list[Token] = []
        while not self.isAtEnd():
            token: Token | None = self.makeToken()
            if token is not None:
                tokens.append(token)
        if self.indentLevel > 0:
            for _ in range(0, self.indentLevel):
                tokens.append(Token(self.lineNumber, TokenType.DEDENT))
        return tokens
