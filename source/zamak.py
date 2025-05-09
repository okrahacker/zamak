# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from lexer import Lexer, Token, TokenType
from parser import Parser
from typechecker import TypeChecker, DataType
from resolver import NameResolver
from trees import *
import sys


ZAMAK_COMPILER_VERSION = '0.0.1'


def printHelpInfo():
    print('Usage: zamak [options] file...\n'
          'Options:\n'
          '    -h, --help:    Show this help message.\n'
          '    -v, --version: Show compiler version information.')

def printVersionInfo():
    print(f'Zamak Compiler version {ZAMAK_COMPILER_VERSION}\n'
           'Copyright (c) 2025, Joseph Hargis. All rights reserved.\n'
           'Licensed under the BSD 2-Clause License.')

def printIncorrectUsage():
    print('Incorrect usage. Run "zamak --help" for correct usage.')


class ArgumentParser:
    OPTIONS: list[str] = ['-h', '--help', '-v', '--version',
                          '-c', '--compile']

    def __init__(self):
        self.options: dict[str, str | bool | list[str]] = {}
        self.index = 1
    
    def isAtEnd(self) -> bool:
        return self.index >= len(sys.argv)

    def peek(self) -> str:
        return sys.argv[self.index]
    
    def advance(self) -> str:
        self.index += 1
        return sys.argv[self.index - 1]
    
    def parseNextOption(self) -> None:
        option: str = self.advance()
        if option in ['-h', '--help']:
            self.options['--help'] = True
        elif option in ['-v', '--version']:
            self.options['--version'] = True
        elif option in ['-c', '--compile']:
            fileNames: list[str] = []
            while not self.isAtEnd() and self.peek() not in self.OPTIONS:
                fileNames.append(self.advance())
            if len(fileNames) == 0:
                printIncorrectUsage()
                quit(1)
            if '--compile' in self.options:
                assert type(self.options['--compile']) == list
                self.options['--compile'] += fileNames
            else:
                self.options['--compile'] = fileNames
        else:
            printIncorrectUsage()
            quit(1)

    def run(self) -> dict[str, str | bool | list[str]]:
        while not self.isAtEnd():
            self.parseNextOption()

        return self.options


def compileSourceCode(sourceCode: str):
    lexer = Lexer()
    tokens: list[Token] = lexer.run(sourceCode)
    print('tokens:')
    previousLineNumber: int = 0
    for token in tokens:
        if token.lineNumber != previousLineNumber:
            previousLineNumber = token.lineNumber
            print(f'    line {previousLineNumber}:')
        match token.category:
            case TokenType.IDENTIFIER:
                print(f'     | IDENTIFIER: {token.lexeme}')
            case TokenType.KEYWORD:
                print(f'     | KEYWORD: {token.lexeme}')
            case TokenType.INDENT:
                print(f'     | INDENT')
            case TokenType.DEDENT:
                print(f'     | DEDENT')
            case TokenType.INTEGER_LIT:
                print(f'     | INTEGER LIT: {token.lexeme}')
            case TokenType.BOOLEAN_LIT:
                print(f'     | BOOLEAN LIT: {token.lexeme}')
            case TokenType.STRING_LIT:
                print(f"     | STRING LIT: '{token.lexeme}'")
            case TokenType.FLOAT_LIT:
                print(f'     | FLOAT LIT: {token.lexeme}')
            case _:
                print(f'     | {token.lexeme}')
    print('')
    parser = Parser()
    trees: list[Stmt] = parser.run(tokens)
    print('trees:')
    for tree in trees:
        print(f'    {tree}')
    nameResolver = NameResolver()
    identifiers: dict[str, DataType] = nameResolver.run(trees)
    typeChecker = TypeChecker()
    typeChecker.run(trees, identifiers)


def compileFiles(fileNames: list[str]):
    for fileName in fileNames:
        sourceCode: str = ''
        with open(fileName, 'r') as sourceFile:
            sourceCode = sourceFile.read()
        compileSourceCode(sourceCode)


def main():
    argumentParser = ArgumentParser()
    options = argumentParser.run()
    if '--help' in options:
        printHelpInfo()
    elif '--version' in options:
        printVersionInfo()
    elif '--compile' in options:
        assert type(options['--compile']) == list, 'Invlaid code path.'
        compileFiles(options['--compile'])
    else:
        # This should never happen.
        assert False, 'Invalid code path.'


if __name__ == '__main__':
    main()