from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]


def hash_(step):
    v = 0
    for c in step:
        v += ord(c)
        v *= 17
        v %= 256

    return v


print(sum(map(hash_, data.split(','))))

from collections import defaultdict

boxes = defaultdict(dict)
for step in data.split(','):
    if '=' in step:
        z, n = step.split('=')
        boxes[hash_(z)][z] = int(n)
    else:
        z = step[:-1]
        if z in (box:=boxes[hash_(z)]):
            del box[z]

q = 0
for box_num, box in boxes.items():
    box_num += 1
    for slot, length in enumerate(box.values(), 1):
        q += box_num * slot * length

print(q)
