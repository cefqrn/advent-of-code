from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

import re
row, column = map(lambda x: int(x) - 1, re.findall(r"\d+", s))
line = row + column

code = 20151125

print(code * pow(252533, line * (line + 1) // 2 + column, 33554393) % 33554393)

for i in range(line * (line + 1) // 2 + column):
    code = code * 252533 % 33554393

print(code)
