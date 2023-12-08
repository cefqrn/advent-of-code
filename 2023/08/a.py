from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

a, b = blocks

from re import findall

a, = a
a = a*10000

paths = {}

for line in b:
    x, y, z = findall(r"\w+", line)
    paths[x] = (y, z)

current = "AAA"
x = 0
for instruction in a:
    current = paths[current]["LR".find(instruction)]
    x += 1
    if current == "ZZZ":
        print(x)
        break

starting = []

for line in b:
    x, y, z= findall(r"\w+", line)
    if x[2] == 'A':
        starting.append((x, 0))
    paths[x] = (y, z)

times = []
for s in starting:
    current = s[0]

    x = 0
    for instruction in a:
        current = paths[current]["LR".find(instruction)]
        x += 1
        if current[2] == "Z":
            times.append(x)
            break

from math import lcm
print(lcm(*times))
