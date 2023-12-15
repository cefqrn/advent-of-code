from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from re import findall

counts = [1] * len(lines)
p1 = 0
for i, line in enumerate(lines, 1):
    count = len(findall(r"(?= (\d+) .* \1\b)", line))
    for j in range(count):
        counts[i+j+1] += counts[i]

    p1 += 2 ** (count - 1) if count else 0

print(p1, sum(counts))
