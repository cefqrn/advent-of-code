import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *

h = 2000000

impossible = set()
beacons = set()
for line in lines:
    x, y, bx, by = get_ints(line)
    beacons.add((bx, by))

    dx = abs(x-bx)
    dy = abs(y-by)
    d = dx + dy

    for nx in range(x-d, x+d+1):
        if manhattan((x, y), (nx, h)) <= d:
            impossible.add((nx, h))
    
    print(line)

print(len(impossible))
print(len(impossible - beacons))

# not 7285196
# not 3760540
# not 5543957
