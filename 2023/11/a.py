from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

empty_rows = set()
empty_columns = set()

for i, line in enumerate(lines):
    if len(set(line)) == 1:
        empty_rows.add(i)

columns = zip(*lines)
for i, line in enumerate(columns):
    if len(set(line)) == 1:
        empty_columns.add(i)

galaxies = set()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c != '.':
            galaxies.add((y, x))

from itertools import combinations

for n in 2, 1000000:
    s = 0
    for (y1, x1), (y2, x2) in combinations(galaxies, r=2):
        lo_y, hi_y = sorted([y1, y2])
        dy = hi_y - lo_y + sum((n-1) for y in range(lo_y, hi_y) if y in empty_rows)
        lo_x, hi_x = sorted([x1, x2])
        dx = hi_x - lo_x + sum((n-1) for x in range(lo_x, hi_x) if x in empty_columns)

        s += dy + dx

    print(s)
