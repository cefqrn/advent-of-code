from collections import deque
from itertools import product
from copy import deepcopy

with open(0) as f:
    instructions = f.readlines()

height = 6
width = 50

screen = [deque([0]) * width for _ in range(height)]

for instruction in instructions:
    match(instruction.split()):
        case "rect", dimensions:
            x, y = map(int, dimensions.split('x'))
            for i, j in product(range(x), range(y)):
                screen[j][i] = 1
        case "rotate", "row", y, _, r:
            y = int(y[2:])
            r = int(r)
            screen[y].rotate(r)
        case "rotate", "column", x, _, r:
            x = int(x[2:])
            r = int(r)
            prev_screen = deepcopy(screen)
            for y in range(height):
                screen[y][x] = prev_screen[y-r][x]
        case _:
            raise ValueError

print(sum(sum(x) for x in screen))
print('\n'.join(''.join(map(" #".__getitem__, x)) for x in screen))
