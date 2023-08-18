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

import re

a = 0
b = 0
c = 0
for l in s.strip().split('\n'):
    a += len(l)
    b += len(eval(l))
    c += len('"' + l.replace('\\', '\\\\').replace('"', '\\"') + '"')

print(a-b)
print(c-a)