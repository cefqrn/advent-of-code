# unfinished

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

from aoclib.point import Point
from re import *

WIDTH = 4

UP     = Point( 0, -1)
DOWN   = Point( 0,  1)
RIGHT  = Point( 1,  0)
LEFT   = Point(-1,  0)


def get_new_pos(position: Point, direction: Point) -> tuple[Point, Point]:
    if direction == LEFT:
        if position.y < 50:
            return Point(0, 149 - position.y), RIGHT
        if position.y < 100:
            return Point((position.y - 50), 100), DOWN
        if position.y < 150:
            return Point(50, 49 - (position.y - 100)), RIGHT
        if position.y < 200:
            return Point(50 + (position.y - 150), 0), DOWN

    if direction == RIGHT:
        if position.y < 50:
            return Point(99, 149 - position.y), LEFT
        if position.y < 100:
            return Point(100 + (position.y - 50), 49), UP
        if position.y < 150:
            return Point(149, 49 - (position.y - 100)), LEFT
        if position.y < 200:
            return Point((position.y - 150) + 50, 149), UP

    if direction == UP:
        if position.x < 50:
            return Point(50, 50 + position.x), RIGHT
        if position.x < 100:
            return Point(0, 150 + (position.x - 50)), RIGHT
        if position.x < 150:
            return Point(position.x - 100, 199), UP
    
    # south
    if position.x < 50:
        return Point(position.x + 100, 0), DOWN
    if position.x < 100:
        return Point(49, 150 + (position.x - 50)), LEFT
    if position.x < 150:
        return Point(99, 50 + (position.x - 100)), LEFT

    raise ValueError


def move(position: Point, direction: Point) -> tuple[Point, Point]:
    new_pos = position + direction

    if new_pos not in grid or grid[new_pos] == ' ':
        new_pos, new_direction = get_new_pos(new_pos, direction)
    else:
        new_direction = direction

    if grid[new_pos] == '#':
        return position, direction

    return new_pos, new_direction
        


block_a, block_b = blocks

grid = {}
position = None
for i, line in enumerate(get_lines(block_a)):
    for j, c in enumerate(line):
        if position is None and c == '.':
            position = Point(j, i)

        grid[Point(j, i)] = c

if position is None:
    raise ValueError


direction = Point(1, 0)
for instruction in findall(r'[\d]+|[RL]', block_b):
    print(f"{instruction:>2}", position, direction)

    if instruction.isnumeric():
        dist = int(instruction)
        for i in range(dist):
            position, direction = move(position, direction)
    else:
        if instruction == 'R':
            direction = direction.rotated(-90)
        else:
            direction = direction.rotated(90)

column, row = position + Point(1, 1)
facing = [RIGHT, DOWN, LEFT, UP].index(direction)

print(1000 * row + 4 * column + facing)


# not 177026 (too high)
# not 26461  (too low)