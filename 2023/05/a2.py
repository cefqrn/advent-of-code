from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

seeds, *blocks = blocks
seeds = tuple(map(int, seeds[0].split()[1:]))

seed_ranges = [range(a, a+b) for a, b in zip(*2*[iter(seeds)])]

conversions = [[tuple(map(int, y.split())) for y in x[1:]] for x in blocks]
reversed_conversions = conversions[::-1]

from contextlib import suppress
from itertools import count

for location_number in count():
    print(location_number)
    print()
    x = location_number
    for conversion in reversed_conversions:
        for a, b, c in conversion:
            with suppress(ValueError):
                x = range(b, b+c)[range(a, a+c).index(x)]
                break

        print(x)

    for r in seed_ranges:
        if x in r:
            print(location_number)
            exit()
