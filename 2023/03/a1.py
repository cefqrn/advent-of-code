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

p1 = 0
seen = set()
for y, line in enumerate(lines):
    for x, n in enumerate(line):
        if not n.isdigit():
            continue

        for dx, dy in product(range(-1, 2), repeat=2):
            if dx == dy == 0:
                continue

            nx, ny = x+dx, y+dy
            if nx < 0 or nx >= len(line) or ny < 0 or ny >= len(lines):
                continue

            if lines[ny][nx] != '.' and not lines[ny][nx].isdigit():
                break
        else:
            continue

        while x >= 0 and line[x].isdigit():
            x -= 1

        x += 1

        if (x, y) in seen:
            continue

        seen.add((x, y))

        c = 0
        while x < len(line) and line[x].isdigit():
            c = c*10 + int(line[x])
            x += 1

        p1 += c

print(p1)
