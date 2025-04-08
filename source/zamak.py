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

def parseArguments() -> dict[str, str | bool] | Error:
    if len(sys.argv) < 2:
        printIncorrectUsage()
        return Error()
    options: dict[str, str | bool] = {}
    currentIndex = 1
    while currentIndex < len(sys.argv):
        argument = sys.argv[currentIndex]
        if argument in ['-h', '--help']:
            options[argument] = True
            currentIndex += 1
        elif argument in ['-v', '--version']:
            options[argument] = True
            currentIndex += 1
        else:
            printIncorrectUsage()
            return Error()
    return options


def main():
    options = parseArguments()
    if isinstance(options, Error):
        return
    elif '-h' in options or '--help' in options:
        printHelpInfo()
        return
    elif '-v' in options or '--version' in options:
        printVersionInfo()
        return


if __name__ == '__main__':
    main()