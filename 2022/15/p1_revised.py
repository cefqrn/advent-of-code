from bisect import insort
from re import findall


def combine_ranges(ranges):
    new_ranges = []

    prev = ranges[0]
    for curr in ranges[1:]:
        if prev[1] < curr[0] - 1:
            new_ranges.append(prev)
            prev = curr
            continue

        prev = (prev[0], max(prev[1], curr[1]))
    
    if not new_ranges or new_ranges[-1] != prev:
        new_ranges.append(prev)
    
    return new_ranges


scanners = []
beacons = set()
with open(0) as f:
    for i, line in enumerate(f.readlines()):
        x, y, bx, by = map(int, findall(r"[-+]?\d+", line))
        beacons.add((bx, by))

        dist = abs(x-bx) + abs(y-by)

        scanners.append((x, y, dist))

ranges = []
h = 2000000
for x, y, d in scanners:
    if (dh:=abs(y-h)) > d:
        continue

    insort(ranges, (x - (d - dh), x + (d - dh)))

s = 0
for lo, hi in combine_ranges(ranges):
    s += hi - lo + 1

for _, by in beacons:
    if by == 2000000:
        s -= 1

print(s)
