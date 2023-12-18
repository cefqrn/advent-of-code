from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from functools import partial
from itertools import pairwise, chain
from operator import mul

# NESW URDL
directions = [
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
    ( 0, -1)
]


def calculate_area(vertices):
    first_vertex = next(vertices)

    return 1 + abs(sum(
        x0*y1 - y0*x1 + abs(y1-y0) + abs(x1-x0)
        for (y0, x0), (y1, x1)
        in pairwise(chain([first_vertex], vertices, [first_vertex]))
    )) // 2


def parse_instructions_1(lines):
    yield from (
        (directions["URDL".index(d)], int(l))
        for d, l, _ in map(str.split, lines)
    )


def parse_instructions_2(lines):
    yield from (
        (directions["URDL".index("RDLU"[int(c[7])])], int(c[2:7], 16))
        for _, _, c in map(str.split, lines)
    )


def get_vertices(instructions):
    y, x = 0, 0
    yield y, x

    for direction, length in instructions:
        dy, dx = map(partial(mul, length), direction)

        yield (y := y+dy, x := x+dx)


print(calculate_area(get_vertices(parse_instructions_1(lines))))
print(calculate_area(get_vertices(parse_instructions_2(lines))))
