import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

from itertools import takewhile

s = 0
for i, line in enumerate(lines):
    for j, tree in enumerate(line):
        lazy_max = lambda x: max(x, default=chr(0))

        s += min(
            lazy_max(line[:j]),
            lazy_max(line[j+1:]),
            lazy_max(lines_transposed[j][:i]),
            lazy_max(lines_transposed[j][i+1:])
        ) < tree

print(s)

s = 0
best = 0
for i, line in enumerate(lines):
    for j, tree in enumerate(line):
        len_shorter = lambda l: len(list(takewhile(lambda x: x < tree, l)))

        right  = len_shorter(line[j+1:])
        left   = len_shorter(line[:j][::-1])
        top    = len_shorter(lines_transposed[j][i+1:])
        bottom = len_shorter(lines_transposed[j][:i][::-1])

        # count tree that blocks view
        right  += right  < len(line[j+1:])
        left   += left   < len(line[:j][::-1])
        top    += top    < len(lines_transposed[j][i+1:])
        bottom += bottom < len(lines_transposed[j][:i][::-1])

        curr = right * left * top * bottom

        if curr > best:
            best = curr

print(best)
