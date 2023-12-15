from contextlib import suppress
from itertools import groupby, pairwise
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

all_values = []
for line in lines:
    *values, = map(int, line.split())
    all_values.append(values)

p1 = p2 = 0

get_diff = lambda a: a[1] - a[0]
for line in all_values:
    differences = [line]
    while any(differences[-1]):
        differences.append(list(map(get_diff, pairwise(differences[-1]))))

    for a, b in pairwise(differences[::-1]):
        b[:0] = b[0] - a[0],
        b += b[-1] + a[-1],

    p1 += differences[0][0]
    p2 += differences[0][-1]

print(p1, p2)
