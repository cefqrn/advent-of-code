from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from collections import defaultdict

counts = defaultdict(lambda: 1)

p1 = 0
for i, line in enumerate(lines, 1):
    if i not in counts:
        counts[i] = 1

    card, numbers = line.split(":")
    winning, have = map(set, map(str.split, numbers.split("|")))

    count = len(winning & have)
    for j in range(1, count+1):
        counts[j+i] += 1 * counts[i]

    x = 2 ** (len(winning & have) - 1)
    if isinstance(x, float):
        x = 0
    p1 += x

print(p1, sum(counts.values()))
