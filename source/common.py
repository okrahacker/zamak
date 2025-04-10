# Copyright (c) 2025, Joseph Hargis. All rights reserved. See LICENSE for details.


class Error:
    pass


def reportError(lineNumber: int, message: str):
    print(f'Error on line {lineNumber}: {message}')
    quit(1)