from contextlib import suppress
from itertools import groupby
from pathlib import Path

with open(Path(__file__).parent / "input") as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

p1 = 0
for line in lines:
    game_id, colors = line.split(": ")

    for color_set in colors.split("; "):
        amounts = {}
        for x in color_set.split(", "):
            n, color = x.split()
            amounts[color] = int(n)

        if amounts.get("red", 0) > 12 or amounts.get("green", 0) > 13 or amounts.get("blue", 0) > 14:
            break
    else:
        p1 += int(game_id[4:])

print(p1)

from math import prod

p1 = 0
for line in lines:
    game_id, colors = line.split(": ")

    amounts = {}
    for color_set in colors.split("; "):
        for x in color_set.split(", "):
            n, color = x.split()
            amounts[color] = max(amounts.get(color, 0), int(n))
    else:
        p1 += prod(amounts.values())

print(p1)
