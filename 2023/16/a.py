from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]


def calculate(sp, sd):
    beams = [(sp, sd)]

    energized = set()
    seen = set()

    while beams:
        position, direction = beams.pop()

        if (position, direction) in seen:
            continue
        seen.add((position,direction))

        y, x = position

        dy, dx = direction
        np = ny, nx = y+dy, x+dx

        if ny not in range(len(lines)) or nx not in range(len(lines[0])):
            continue
        energized.add(np)

        match lines[ny][nx]:
            case "|":
                if directions.index(direction) & 1:
                    beams.append((np, directions[0]))
                    beams.append((np, directions[2]))
                else:
                    beams.append((np, direction))
            case "-":
                if directions.index(direction) & 1:
                    beams.append((np, direction))
                else:
                    beams.append((np, directions[3]))
                    beams.append((np, directions[1]))
            case "/":
                ndy, ndx = -dx, -dy
                beams.append((np, (ndy, ndx)))
                continue
            case "\\":
                ndy, ndx = dx, dy
                beams.append((np, (ndy, ndx)))
                continue
            case ".":
                beams.append((np, direction))
            case _:
                raise ValueError

    return(len(energized))

m = 0

width = len(lines[0])
height = len(lines)

for y in range(height):
    m = max(m,calculate((y, -1), (0, 1)))
    m = max(m,calculate((y, width), (0, -1)))

for x in range(width):
    m = max(m,calculate((-1, x), (1, 0)))
    m = max(m,calculate((height, x), (-1, 0)))

print(calculate((0, -1), (0, 1)), m)
