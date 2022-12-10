import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

x=1

view = []


row = 0
cycle = 0
def new_cycle():
    global cycle, view

    cycle += 1

    if cycle % 40 == 1:
        view.append([" "]*50)

    if ~-cycle%40 in range(x-1, x+2):
        view[-1][cycle%40] = "#"
    else:
        view[-1][cycle%40] = " "


for i, line in enumerate(lines):
    match line.split():
        case ["noop"]:
            new_cycle()
        case ["addx", v]:
            new_cycle()
            new_cycle()
            x += int(v)

print('\n'.join(map(' '.join, (view))))
