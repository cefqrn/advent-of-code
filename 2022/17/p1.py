import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib import *
from itertools import cycle

rocks: list[tuple[tuple[int, int], ...]] = [
    ((2, 0), (3, 0), (4, 0), (5, 0)),
    ((2, 1), (3, 0), (3, 1), (3, 2), (4, 1)),
    ((2, 0), (3, 0), (4, 0), (4, 1), (4, 2)),
    ((2, 0), (2, 1), (2, 2), (2, 3)),
    ((2, 0), (2, 1), (3, 0), (3, 1))
]

g = [["."] * 7 for _ in range(1000)]
def move_rock(rock, direction):
    if direction == 'v':
        for x, y in rock:
            if y-1 < 0:
                raise ValueError
            if g[y-1][x] != ".":
                raise ValueError
        
        return tuple((x, y-1) for x, y in rock)
    elif direction == '>':
        for x, y in rock:
            if g[y][x+1] != ".":
                raise IndexError

        return tuple((x+1, y) for x, y in rock) 
    elif direction == '<':
        for x, y in rock:
            if x-1 < 0:
                raise IndexError
            if g[y][x-1] != ".":
                raise IndexError
            
        return tuple((x-1, y) for x, y in rock)
    else:
        raise KeyError


wind_index = -1
max_height = 0

prev_heights = [max_height]

for i, rock in enumerate(cycle(rocks)):
    if i == 25:
        break

    if max_height > 67:
        print(i)

    rock = tuple((x, y + max_height+3) for x, y in rock)

    try:
        while True:
            try:
                wind_index += 1
                rock = move_rock(rock, input_string[wind_index % len(input_string)])
            except IndexError:
                pass
            rock = move_rock(rock, 'v')
    except ValueError:
        pass

    for x, y in rock:
        if y + 1 > max_height:
            max_height = y + 1

    prev_heights.append(max_height)

    for x, y in rock:
        g[y][x] = "O"

    # grid.print_grid(list(reversed(g)))

    # break


print(max_height)
grid.print_grid(list(reversed(g)))
