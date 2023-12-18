from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

# NESW
directions = [
    -1 + 0j, # U
     0 + 1j, # R
     1 + 0j, # D
     0 - 1j  # L
]

pos = 0 + 0j
dug = set()

for d, l, c in map(str.split, lines):
    dug.add(pos)
    for i in range(int(l)):
        pos += directions["URDL".index(d)]
        dug.add(pos)

lo_y = min(int(x.real) for x in dug)
hi_y = max(int(x.real) for x in dug)
lo_x = min(int(x.imag) for x in dug)
hi_x = max(int(x.imag) for x in dug)


def count(initial):
    new_dug = dug.copy()

    remaining = [initial]
    while remaining:
        pos = remaining.pop()

        if pos in new_dug:
            continue
        new_dug.add(pos)

        # if it escapes the bounds
        if pos.real not in range(lo_y, hi_y+1) or pos.imag not in range(lo_x, hi_x+1):
            raise ValueError

        for direction in directions:
            remaining.append(pos + direction)

    return len(new_dug)


for i in range(-5, 5):
    for j in range(-5, 5):
        pos = i + j*1j
        if pos in dug:
            continue

        try:
            print(count(pos))
        except ValueError:
            continue

        break
