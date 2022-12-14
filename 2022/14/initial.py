import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *

highest_y = INFINITY_NEGATIVE

grid = [[" "] * 1000 for _ in range(1000)]
for line in lines:
    ints = get_ints(line)
    for (a, b), (c, d) in zip(zip(ints[::2], ints[1::2]), zip(ints[2::2], ints[3::2])):
        for x in range(min(a,c), max(a,c)+1):
            for y in range(min(b,d), max(b,d)+1):
                if y > highest_y:
                    highest_y = y
                grid[y][x] = "#"

highest_y += 2
p1_done = False

i = 0


def next_coord(x, y):
    global highest_y, p1_done

    if y + 1 == highest_y:
        if not p1_done:
            print(f"p1: {i}")
            p1_done = True
        return x, y

    if grid[y+1][x] == " ":
        return x, y + 1

    if grid[y+1][x-1] == " ":
        return x - 1, y + 1
    
    if grid[y+1][x+1] == " ":
        return x + 1, y + 1
    
    return x, y


while True:
    x, y = 500, 0

    while (n:=next_coord(x, y)) != (x, y):
        x, y = n
    
    grid[y][x] = "o"

    i += 1

    if (x, y) == (500, 0):
        print(f"p2: {i}")
        break