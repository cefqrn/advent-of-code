from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from collections import defaultdict

points =lines

animal_position = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == 'S':
            animal_position = y, x


from grid import neighbor_indices

def get_offsets(spot):
    match (spot):
        case '|':
            return (-1, 0), (1, 0)
        case '-':
            return (0, 1), (0, -1)
        case 'L':
            return (-1, 0), (0, 1)
        case 'J':
            return (-1, 0), (0, -1)
        case '7':
            return (0, -1), (1, 0)
        case 'F':
            return (0, 1), (1, 0)
        case 'S':
            return (1, 0), (-1, 0), (0, -1), (0, 1)
        case '.':
            return ()


seen = defaultdict(lambda: float("inf"))
seen[animal_position] = 0
# y, x, distance
loop_positions = [(*animal_position, 0)]
while loop_positions:
    y, x, d = loop_positions.pop()

    offsets = get_offsets(points[y][x])

    nd = d+1
    for ny, nx in neighbor_indices(points, x, y, offsets):
        neighbor = points[ny][nx]
        neighbor_offsets = get_offsets(neighbor)

        if (y, x) not in {(ny+dy, nx+dx) for dy, dx in neighbor_offsets}:
            continue

        if seen[(ny, nx)] <= nd:
            continue
        seen[(ny, nx)] = nd
        loop_positions.append(
            (ny, nx, nd)
        )

print(max(seen.values()))
