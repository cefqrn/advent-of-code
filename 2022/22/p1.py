import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

from aoclib.point import Point
from re import *

direction = Point(1, 0)


block_a, block_b = blocks


grid = {}
for i, line in enumerate(get_lines(block_a)):
    for j, c in enumerate(line):
        grid[Point(j, i)] = c



def move(position: Point, direction: Point) -> Point:
    try:
        if direction[0]:
            new_pos = Point((position + direction).x, position.y)
            if new_pos not in grid or grid[new_pos] == ' ':
                if direction.x == 1:
                    for i, c in enumerate(lines[position.y]):  # type: ignore
                        if c != ' ':
                            new_pos = Point(i, position.y)
                            break
                else:
                    for i, c in enumerate(reversed(lines[position.y])):  # type: ignore
                        if c != ' ':
                            new_pos = Point(len(lines[position.y])+~i, position.y)    # type: ignore
                            break
        else:
            new_pos = Point(position.x, (position + direction).y)
            if new_pos not in grid or grid[new_pos] == ' ':
                if direction.y == 1:
                    for i, c in enumerate(line[position.x] for line in lines):  # type: ignore
                        if c != ' ':
                            new_pos = Point(position.x, i)
                            break
                else:
                    l = [line.ljust(position.x+1)[position.x] for line in block_a.split('\n')]    # type: ignore
                    for i, c in enumerate(reversed(l)):  # type: ignore
                        if c != ' ':
                            new_pos = Point(position.x, len(l)+~i)
                            break

        if grid[new_pos] == '#':
            raise ValueError

        return new_pos
    except ValueError:  # hit wall
        print('hit wall')
        return position

pos = move(Point(0, 0), direction)

print(pos, direction)
for instruction in findall(r'[\d]+|[RL]', block_b):
    if instruction.isnumeric():
        dist = int(instruction)
        for i in range(dist):
            new_pos = move(pos, direction)
            if new_pos == pos:
                break
            pos = new_pos
    else:
        if instruction == 'R':
            direction = direction.rotated(-90)
        else:
            direction = direction.rotated(90)

    print(f"{instruction:>2}", pos, direction)

column, row = pos + Point(1, 1)
facing = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)].index(direction)

print(1000 * row + 4 * column + facing)

# not 4206    forgot about wrapping left and up
# not 150214  whoops used direction.x for wrapping y
