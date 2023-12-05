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

conversions = [[tuple(map(int, y.split())) for y in x[1:]] for x in blocks]

locations = []
for seed in seeds:
    x = seed
    for conversion in conversions:
        for a, b, c in conversion:
            with suppress(ValueError):
                x = range(a, a+c)[range(b, b+c).index(x)]
                break

    locations.append(x)

print(min(locations))
