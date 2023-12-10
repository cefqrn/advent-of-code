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
from math import inf

points =lines

animal_position = None
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == 'S':
            animal_position = y, x

from grid import neighbor_indices, VON_NEUMANN_NEIGHBORHOOD
from itertools import chain

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

from operator import neg, sub
def connected_sides(spot, direction):
    match (spot):
        case '|':
            return direction,
        case '-':
            return direction,
        case 'L':
            return ((-1, 0), (0, 1)) if direction in {(-1, 0), (0, 1)} else ((1, 0), (0, -1))
        case 'J':
            return ((-1, 0), (0, -1)) if direction in {(-1, 0), (0, -1)} else ((1, 0), (0, 1))
        case '7':
            return ((0, -1), (1, 0)) if direction in {(0, -1), (1, 0)} else ((0, 1), (-1, 0))
        case 'F':
            return ((0, 1), (1, 0)) if direction in {(0, 1), (1, 0)} else ((0, -1), (-1, 0))
        case 'S':
            return ()
        case '.':
            raise ValueError

    return (tuple(map(neg, coord)) for coord in get_offsets(spot))


seen = defaultdict(lambda: inf)
seen[animal_position] = 0
# y, x, distance
remaining = [(*animal_position, 0)]
while remaining:
    y, x, d = remaining.pop()

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

        remaining.append(
            (ny, nx, nd)
        )

def is_on_loop(y, x):
    return seen[(y, x)] < inf

initial = (-1, 0)


seen2 = defaultdict(lambda: inf)
seen2[initial] = 0

directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]

remaining = [(*initial, 0)]
first_pipe = None
while remaining:
    y, x, d = remaining.pop()
    nd = d+1

    for ny, nx in neighbor_indices(points, x, y, directions):
        if seen2[(ny, nx)] <= nd:
            continue
        seen2[(ny, nx)] = nd

        if is_on_loop(ny, nx) and lines[ny][nx] != 'S':
            # direction of the inside
            direction = tuple(map(sub, (ny, nx), (y, x)))
            first_pipe = (
                ny, nx, connected_sides(lines[ny][nx], direction)
            )
            break
        elif lines[ny][nx] != 'S':
            remaining.append((
                ny, nx, nd
            ))
    else:
        continue
    break

seen3 = set()
remaining = [first_pipe]
to_check = set()
while remaining:
    y, x, outside = remaining.pop()
    for ny, nx in neighbor_indices(lines, x, y, outside):
        if is_on_loop(ny, nx):
            continue

        to_check.add((ny, nx))

    if lines[y][x] == 'S':
        continue

    for dy, dx in get_offsets(lines[y][x]):
        ny, nx = y+dy, x+dx
        if not is_on_loop(ny, nx):
            raise ValueError

        if (ny, nx) in seen3:
            continue

        seen3.add((ny, nx))

        if dy:
            # keep horizontal diretions
            horizontal_directions = [x for x in outside if x in directions[1::2]]
            remaining.append((ny, nx,
                list(set(horizontal_directions + list(chain.from_iterable(
                    connected_sides(lines[ny][nx], x) for x in horizontal_directions
            ))))))
        if dx:
            # keep vertical directions
            vertical_directions = [x for x in outside if x in directions[::2]]
            remaining.append((ny, nx,
                list(set(vertical_directions + list(chain.from_iterable(
                    connected_sides(lines[ny][nx], x) for x in vertical_directions
            ))))))

inside = set(to_check)
while to_check:
    y, x = to_check.pop()
    for ny, nx in neighbor_indices(lines, x, y, VON_NEUMANN_NEIGHBORHOOD):
        if is_on_loop(ny, nx):
            continue

        if (ny, nx) in inside:
            continue
        inside.add((ny, nx))

        to_check.add((ny, nx))

print(len(inside))
