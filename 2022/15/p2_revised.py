from bisect import insort
from time import perf_counter
from re import findall

st = perf_counter()


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
with open(0) as f:
    for line in f.readlines():
        x, y, bx, by = map(int, findall(r"[-+]?\d+", line))
        d = abs(x-bx) + abs(y-by)

        scanners.append((x, y, d))


for h in range(4000000):
    ranges = []
    for x, y, d in scanners:
        if (dh:=abs(y-h)) > d:
            continue

        insort(ranges, (x - (d - dh), x + (d - dh)))

    ranges = combine_ranges(ranges)

    if len(ranges) > 1:
        x, y = ranges[1][0] - 1, h
        print(x, y, x*4000000 + h)
        break

print(perf_counter() - st)
