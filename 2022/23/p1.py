import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *
from aoclib.pathfinding import MOORE
from aoclib.grid import print_grid
from aoclib.point import Point

grid = [list("." * (len(lines[0])+ 40)) for _ in range(20)]
grid = [*grid, *[list("."*20 + line + "."*20) for line in lines], *grid]

def check_prop(pos, *distances):
    global propositions, tried, not_moving

    for d in distances:
        n = nx, ny = pos + Point(*d)
        try:
            if nx < 0 or ny < 0: raise IndexError
            if grid[ny][nx] == '#':
                return 0  # there's a neighbor, keep looking
        except IndexError:
            pass
    else:
        if nx < 0 or ny < 0: raise IndexError
        grid[ny][nx]  # just check if in bounds (indexerrors if out)

        if (n in tried):
            if n in propositions:
                not_moving.add(propositions[n])
                not_moving.add(pos)
                del propositions[n]

            return 1  # stop looking for more, there was a collision

        tried.add(n)
        propositions[n] = pos

        return 1  # successful

DIRECTIONS = [
    (( 1, -1), (-1, -1), ( 0, -1)),
    (( 1,  1), (-1,  1), ( 0,  1)),
    ((-1,  1), (-1, -1), (-1,  0)),
    (( 1,  1), ( 1, -1), ( 1,  0)),
]

direction_offset = 0

def iterate():
    global propositions, tried, not_moving, direction_offset
    not_moving = set()
    propositions = {}
    tried = set()

    new_grid = [list("."*len(grid[0])) for _ in range(len(grid))]
    for y, line in enumerate(grid):
        for x, elf in enumerate(line):
            if elf != '#':
                continue

            pos = Point(x, y)

            for d in MOORE:
                nx, ny = pos + Point(*d)

                try:
                    if nx < 0 or ny < 0: raise IndexError
                    if grid[ny][nx] == '#':
                        break
                except IndexError:
                    pass
            else:
                not_moving.add((x, y))
                continue

            pos = Point(x, y)
            if check_prop(pos, *DIRECTIONS[(direction_offset) % 4]): continue
            if check_prop(pos, *DIRECTIONS[(direction_offset+1) % 4]): continue
            if check_prop(pos, *DIRECTIONS[(direction_offset+2) % 4]): continue
            if check_prop(pos, *DIRECTIONS[(direction_offset+3) % 4]): continue

            not_moving.add((x, y))

    for (nx, ny), (x, y) in propositions.items():
        try:
            new_grid[ny][nx] = '#'
        except IndexError:
            not_moving.add((x, y))
            pass

    for x, y in not_moving:
        new_grid[y][x] = '#'

    direction_offset += 1

    if not propositions:
        return new_grid, 0

    return new_grid, 1

moving = 1
while moving:
    grid, moving = iterate()
    # print_grid(grid)
    # print()


minx = 99999999999
miny = 99999999999
maxx = 0
maxy = 0
for y, line in enumerate(grid):
    for x, elf in enumerate(line):
        if elf != '#':
            continue

        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x, maxx)
        maxy = max(y, maxy)

s = 0
for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        if grid[y][x] != '#':
            s += 1

print(minx, maxx,miny, maxy, )

print(s)

# not 2521
