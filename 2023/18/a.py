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
from operator import mul

# NESW URDL
directions = [
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
    ( 0, -1)
]


def calculate_area(instructions):
    twice_area = 0
    pos = 0, 0
    for direction, length in instructions:
        dy, dx = map(partial(mul, length), direction)

        y0, x0 = pos
        y1, x1 = pos = y0+dy, x0+dx

        twice_area += (x0*y1 - y0*x1) + length

    return abs(twice_area >> 1) + 1


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


print(calculate_area(parse_instructions_1(lines)))
print(calculate_area(parse_instructions_2(lines)))
