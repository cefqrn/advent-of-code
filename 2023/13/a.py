from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from operator import eq

def find_reflection(block, ignore=None):
    for i in range(1, len(block)):
        if all(map(eq, block[:i][::-1], block[i:])):
            o = i*100
            if o == ignore:
                continue
            return o

    block = list(zip(*block))
    for i in range(1, len(block)):
        if all(map(eq, block[:i][::-1], block[i:])):
            o = i
            if o == ignore:
                continue
            return o

def p2_reflection(block):
    block = list(map(list, block))
    base = find_reflection(block)

    for line in block:
        for x, _ in enumerate(line):
            line[x] = "#."[".#".find(line[x])]
            r = find_reflection(block, base)
            line[x] = "#."[".#".find(line[x])]

            if r is not None and r != base:
                return r

    raise ValueError

p = q = 0
for i, block in enumerate(blocks):
    p += find_reflection(block)
    q += p2_reflection(block)

print(p, q)
