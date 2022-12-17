import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib import *


h = 2000000

beacons = []
r = intrange.IntRange()
for line in lines:
    x, y, bx, by = parsing.get_ints(line)
    d = abs(x-bx) + abs(y-by)

    beacons.append((bx, by))

    if (dh:=abs(y-h)) > d:
        continue

    r |= intrange.IntRange(x - (d - dh), x + (d - dh))

for bx, by in beacons:
    if by != h:
        continue

    r -= bx

print(len(r))
