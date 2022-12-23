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

block_a, block_b = blocks


grid = {}
initial_position = None
for i, line in enumerate(get_lines(block_a)):
    for j, c in enumerate(line):
        if initial_position is None and c == '.':
            initial_position = Point(j, i)

        grid[Point(j, i)] = c

if initial_position is None:
    raise ValueError

position = initial_position

sides = {}
class Side:
    def __init__(self, coord):
        sides[coord] = self

        self.coord: Point = coord
        self.adjacent: dict[int, tuple[Side, int]] = {}
    
    def find_non_rotated_adjacent(self):
        for i, diff in enumerate([Point(0, -WIDTH), Point(WIDTH, 0), Point(0, WIDTH), Point(-WIDTH, 0)]):
            pos = self.coord + diff
            
            if pos not in grid or grid[pos] == ' ':
                continue

            if pos in sides:
                new_side = sides[pos]
            else:
                new_side = Side(pos)
                new_side.find_non_rotated_adjacent()

            self.adjacent[i] = new_side, 0

        self.find_adjacent_adjacent()

    def find_adjacent_adjacent(self):
        for i, (side, rot) in self.adjacent.items():
            adjacent_i = (i + 1) % 4
            if adjacent_i not in self.adjacent:
                continue

            # current is 1
            # i=0, side is 2, rot is -1
            # adjacent_i is 1
            # adjacent is 3, adjacent_rot is 0
            
            # side.adjacent index is adjacent_i - rot
            # adjacent.adjacent index is i - adjacent_rot

            # side-adjacent_rot = -adjacent_rot - 1
            # adjacent-side_rot = -rot + 1

            # side.adjacent[2] = adjacent, -1
            # adjacent.adjacent[0] = side,  1

            adjacent, adjacent_rot = self.adjacent[adjacent_i]

            print(self, "adds", side, rot, adjacent, adjacent_rot, "rotated", -1 + adjacent_rot, +1 + adjacent_rot)

            side.adjacent[(adjacent_i + rot) % 4]     = adjacent, (-1 + adjacent_rot)
            adjacent.adjacent[(i - adjacent_rot) % 4] = side,     (+1 + adjacent_rot)

    def __repr__(self):
        return f"Side({self.coord.x}, {self.coord.y})"

initial_side = Side(initial_position)
initial_side.find_non_rotated_adjacent()

for i, (_, side) in enumerate(sorted(sides.items())):
    # side.find_adjacent_adjacent()
    grid[side.coord] = str(i)

initial_side.adjacent[3][0].find_adjacent_adjacent()

for y in range(len(block_a.split('\n'))):
    for x in range(WIDTH*4):
        pos = Point(x, y)
        if pos in grid:
            print(grid[pos], end='')
    print()

print(2, initial_side.adjacent)
print(1, initial_side.adjacent[3][0].adjacent)
print(3, initial_side.adjacent[2][0].adjacent)



# def move(position: Point, direction: Point) -> Point:
#     global curr_side
    
#     try:
#         if direction[0]:
#             new_pos = Point((position + direction).x, position.y)
#             if new_pos not in grid or grid[new_pos] == ' ':
#                 if direction.x > 0:
#                     side_index = 1
#                 else:
#                     side_index = 3

#                 new_side, angle = curr_side.adjacent[side_index]
#                 new_pos = (position - curr_side.coord).rotated(90 * angle)
#                 if grid[new_pos] == '#':
#                     raise ValueError

#                 curr_side = new_side
#                 direction = direction.rotated(angle * 90)
#         else:
#             new_pos = Point(position.x, (position + direction).y)
#             if new_pos not in grid or grid[new_pos] == ' ':
#                 if direction.y > 0:
#                     side_index = 2
#                 else:
#                     side_index = 0

#                 new_side, angle = curr_side.adjacent[side_index]
#                 new_pos = (position - curr_side.coord).rotated(90 * angle)
#                 print(new_pos)

#                 if grid[new_pos] == '#':
#                     raise ValueError

#                 curr_side = new_side
#                 direction = direction.rotated(angle * 90)

#         if grid[new_pos] == '#':
#             raise ValueError

#         return new_pos
#     except ValueError:  # hit wall
#         return position



# direction = Point(1, 0)

# # print(initial_position, direction, curr_side)
# for instruction in findall(r'[\d]+|[RL]', block_b):
#     if instruction.isnumeric():
#         dist = int(instruction)
#         for i in range(dist):
#             new_pos = move(position, direction)
#             if new_pos == position:
#                 break
#             position = new_pos
#     else:
#         if instruction == 'R':
#             direction = direction.rotated(-90)
#         else:
#             direction = direction.rotated(90)

#     # print(f"{instruction:>2}", pos, direction)




# # column, row = pos + Point(1, 1)
# # facing = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)].index(direction)

# # print(1000 * row + 4 * column + facing)
