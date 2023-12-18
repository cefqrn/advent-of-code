from contextlib import suppress
from itertools import groupby, chain
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from functools import partial
from itertools import groupby, islice, pairwise, tee
from operator import mul
from bisect import bisect_left

# NESW URDL
directions = [
    (-1,  0),
    ( 0,  1),
    ( 1,  0),
    ( 0, -1)
]


def calculate_area(instructions):
    """
    calculates the area of the polygon
    by separating it into rectangles
    """

    a, b = tee(instructions)
    ys = sorted({y for y, _ in get_vertices(a)})

    # get the walls of all the rectangles
    vertical_walls = []
    x = y = 0
    perimiter = 0
    for direction, length in b:
        perimiter += length
        dy, dx = map(partial(mul, length), direction)

        ny = y+dy
        lo_y, hi_y = sorted([y, ny])

        # the walls are split into multiple segments
        # in case the wall on the other side breaks earlier
        if not directions.index(direction) & 1:
            lo_yi = bisect_left(ys, lo_y)
            hi_yi = bisect_left(ys, hi_y, lo=lo_yi)

            vertical_walls.extend((y0, x, y1-y0) for y0, y1 in pairwise(ys[lo_yi:hi_yi+1]))

        y, x = ny, x+dx

    inner_area = sum(
        (x1 - x0) * height
        for _, g in groupby(sorted(vertical_walls), lambda x: x[0])
        for (_, x0, height), (_, x1, _) in islice(pairwise(g), None, None, 2)
    )

    # test input visualized
    # https://www.desmos.com/calculator/xg9ggndcau
    # then shifted onto the inner area
    # https://www.desmos.com/calculator/rhp1hkzace
    # every flat unit of perimiter contributes 1/2 unit^2 to the area
    # those on the outer corners contribute 3/4 unit^2
    # those on the inner ones contribute 1/4 unit^2
    # so since a cavity has to go in then out
    # and vice versa for an outcropping
    # they can both be reduced to flat surfaces
    # since 2*inner + 2*outer = 2*1/4 + 2*3/4 = 2 = 4 * 1/2 = 4*flat
    # but since the polygon has to be closed
    # there are 4 outer corners that can't be ignored
    # so you have extra area = (perimiter-4) * flat + 4 * outer = (perimiter-4) * 1/2 + 4 * 3/4
    # = perimiter/2 - 2 + 3 = perimiter/2 + 1

    return inner_area + perimiter//2 + 1


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


print(calculate_area(parse_instructions_1(lines)))
print(calculate_area(parse_instructions_2(lines)))
