from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from itertools import starmap
from math import prod, sqrt, ceil, floor


def solve(time, distance):
    # (time - held) * held = distance
    # -1 * held**2 + time * held - distance = 0
    # a, b, c = -1, time, -distance
    # use quadratic formula to solve for held
    lo =  ceil((-time + sqrt(time**2 - 4*distance)) / -2)
    hi = floor((-time - sqrt(time**2 - 4*distance)) / -2)

    return hi - lo + 1


print(
    prod(starmap(solve, zip(*(map(int, x.split()[1:]) for x in lines)))),
    solve(*(int("".join(x.split()[1:])) for x in lines))
)
