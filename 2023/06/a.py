from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from itertools import count
from math import prod


def solve(time, distance):
    beats = 0
    prev = 0
    for held in count():
        current = (time - held) * held
        if current > distance:
            beats += 1
            continue

        if current < prev:
            break

        prev = current

    return beats


print(
    prod(solve(time, distance) for time, distance in zip(*(map(int, x.split()[1:]) for x in lines))),
    solve(*(int("".join(x.split()[1:])) for x in lines))
)
