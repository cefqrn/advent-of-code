import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *
from itertools import product

highest_y = INFINITY_NEGATIVE

grid = set()
for line in lines:
    ints = get_ints(line)
    for (a, b), (c, d) in zip(zip(ints[::2], ints[1::2]), zip(ints[2::2], ints[3::2])):
        a, c = sorted([a, c])
        b, d = sorted([b, d])

        for x, y in product(range(a, c+1), range(b, d+1)):
            if y > highest_y:
                highest_y = y

            grid.add((x, y))

highest_y += 2
at_rest_count = 0


p1_done = False
def next_coord(coord):
    global p1_done

    x, y = coord

    if y + 1 == highest_y:
        if not p1_done:
            print(f"p1: {at_rest_count}")
            p1_done = True

        return coord

    for dx in 0, -1, 1:
        if (x+dx, y+1) not in grid:
            return x + dx, y + 1
    
    return coord

while True:
    coord = 500, 0
    while (n:=next_coord(coord)) != coord:
        coord = n
    
    grid.add(n)

    at_rest_count += 1

    if coord == (500, 0):
        print(f"p2: {at_rest_count}")
        break
