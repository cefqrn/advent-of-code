import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

x=1

vals = []
cycle = 0
for i, line in enumerate(lines):
    match line.split():
        case ["noop"]:
            cycle += 1
            if cycle % 40 == 20:
                vals.append(x)
        case ["addx", v]:
            cycle += 1
            if cycle % 40 == 20:
                vals.append(x)
            cycle += 1
            if cycle % 40 == 20:
                vals.append(x)
            x += int(v)

s = 0
for i, a in enumerate(vals):
    s += (40 * (i)+20) * a

print(s)
