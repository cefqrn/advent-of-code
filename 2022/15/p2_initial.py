import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *

        
def combine_ranges(ranges, other):
    ranges = sorted([*ranges, other])
    new_ranges = []

    for lo, hi in ranges:
        if new_ranges and new_ranges[-1][1] >= lo - 1:
            new_ranges[-1] = (new_ranges[-1][0], max(hi, new_ranges[-1][1]))
        else:
            new_ranges.append((lo, hi))
    
    return new_ranges


for h in range(20):
    ranges = []
    for line in lines:
        x, y, bx, by = get_ints(line)

        dx = abs(x-bx)
        dy = abs(y-by)
        d = dx + dy

        dh = abs(y-h)

        if dh > d:
            continue

        r = (x - (d - dh), x + (d - dh))
        ranges = combine_ranges(ranges, r)
    
    if len(ranges) > 1:
        print((ranges[1][0]-1)*4000000 + h)
