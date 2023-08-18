from sys import stdin, argv
from os import isatty


def read():
    if len(argv) == 2:
        with open(argv[1]) as f:
            s = f.read()
    elif not isatty(0):  # check if stdin is a file
        s = stdin.read()
    else:
        print("input not given")
        exit(1)
    
    return s.strip()


def readlines():
    return read().splitlines()
