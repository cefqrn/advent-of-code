from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from grid import neighbor_indices, neighbors

from collections import defaultdict
from math import prod
from re import finditer, search

p1 = 0

gears = defaultdict(list)
for y, line in enumerate(lines):
    for m in finditer(r"\d+", line):
        value = int(m.group())
        adjacent_gears = set()
        is_part_number = False

        for x in range(*m.span()):
            if search(r"[^\d.]", "".join(neighbors(lines, x, y))) \
                    and not is_part_number:
                is_part_number = True
                p1 += value

            for neighbor in neighbor_indices(lines, x, y):
                if neighbor in adjacent_gears:
                    continue

                ny, nx = neighbor
                if lines[ny][nx] == '*':
                    adjacent_gears.add(neighbor)
                    gears[neighbor].append(value)

p2 = 0
for adjacent_numbers in gears.values():
    if len(adjacent_numbers) == 2:
        p2 += prod(adjacent_numbers)

print(p1, p2)
