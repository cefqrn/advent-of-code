from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from itertools import product
from re import finditer

from collections import defaultdict
ratios = defaultdict(list)
for y, line in enumerate(lines):
    for m in finditer(r"\d+", line):
        number = int(m.group())
        gears = set()
        for x in range(*m.span()):
            for dx, dy in product(range(-1, 2), repeat=2):
                if dx == dy == 0:
                    continue

                nx, ny = x+dx, y+dy
                if nx < 0 or nx >= len(line) or ny < 0 or ny >= len(lines):
                    continue

                if (nx, ny) in gears:
                    continue

                if lines[ny][nx] == '*':
                    gears.add((nx, ny))
                    ratios[(nx, ny)].append(number)

from math import prod
p1 = 0
for a, b in ratios.items():
    if len(b) == 2:
        p1 += prod(b)

print(p1)
