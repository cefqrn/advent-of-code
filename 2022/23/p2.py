import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

from aoclib.pathfinding import MOORE


DIRECTIONS = [
    (( 1, -1), (-1, -1), ( 0, -1)),
    (( 1,  1), (-1,  1), ( 0,  1)),
    ((-1,  1), (-1, -1), (-1,  0)),
    (( 1,  1), ( 1, -1), ( 1,  0)),
]

direction_offset = 0


grid = set()
for y, line in enumerate(lines):
    for x, elf in enumerate(line):
        if elf == '#':
            grid.add((x, y))


def check_prop(pos, *distances):
    global propositions, tried, not_moving

    for d in distances:
        n = pos[0] + d[0], pos[1] + d[1]
        if n in grid:
            return 0  # there's a neighbor, keep looking
    else:
        if n in tried:  # abuse python's scoping rules
            if n in propositions:
                not_moving.add(propositions[n])
                not_moving.add(pos)
                del propositions[n]

            return -1  # stop looking for more, there was a collision

        tried.add(n)
        propositions[n] = pos

        return 1  # successful


def iterate():
    global propositions, tried, not_moving, direction_offset, grid
    not_moving = set()
    propositions = {}
    tried = set()

    new_grid = set()
    for pos in grid:
        x, y = pos

        for d in MOORE:
            n = d[0] + x, d[1] + y

            try:
                if n in grid:
                    break
            except IndexError:
                pass
        else:
            not_moving.add((x, y))
            continue

        if check_prop(pos, *DIRECTIONS[(direction_offset) % 4]): continue
        if check_prop(pos, *DIRECTIONS[(direction_offset+1) % 4]): continue
        if check_prop(pos, *DIRECTIONS[(direction_offset+2) % 4]): continue
        if check_prop(pos, *DIRECTIONS[(direction_offset+3) % 4]): continue

        not_moving.add((x, y))

    new_grid.update(propositions.keys())
    new_grid.update(not_moving)

    direction_offset += 1

    if not propositions:
        return new_grid, 0

    return new_grid, 1


moving = 1
round_num = 0
while moving:
    grid, moving = iterate()
    round_num += 1

print(round_num)
