# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


from common import Error
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
    
    def parseNextOption(self) -> None | Error:
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
                return Error()
            if '--compile' in self.options:
                assert type(self.options['--compile']) == list
                self.options['--compile'] += fileNames
            else:
                self.options['--compile'] = fileNames
        else:
            printIncorrectUsage()
            return Error()

    def run(self) -> dict[str, str | bool | list[str]] | Error:
        while not self.isAtEnd():
            if isinstance(self.parseNextOption(), Error):
                return Error()

        return self.options


def compileSourceCode(fileName: str):
    pass

def compileFiles(fileNames: list[str]):
    for fileName in fileNames:
        sourceCode: str = ''
        with open(fileName, 'r') as sourceFile:
            sourceCode = sourceFile.read()
        print(sourceCode)
        compileSourceCode(sourceCode)


def main():
    argumentParser = ArgumentParser()
    options = argumentParser.run()
    if isinstance(options, Error):
        return
    elif '--help' in options:
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