from __future__ import annotations

from itertools import permutations, product
from typing import NamedTuple
from re import findall

from time import perf_counter

st = perf_counter()

SEARCH_AREA = 20


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"


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


# lines defined by their value at x=0 (slope is 1 or -1)
ranges_a: list[tuple[int, int]] = []  # like / /
ranges_b: list[tuple[int, int]] = []  # like \ \

scanners = []
with open(0) as f:
    for i, line in enumerate(f.readlines()):
        x, y, bx, by = map(int, findall(r"[-+]?\d+", line))
        dist = abs(x-bx) + abs(y-by)

        b, d = Point(x+dist, y), Point(x-dist, y)

        scanners.append((x, y, dist))

        ranges_a.append((b.y-b.x, d.y-d.x))
        ranges_b.append((d.y+d.x, b.y+b.x))

a_candidates = set()
for (lo1, hi1), (lo2, hi2) in permutations(ranges_a, r=2):
    if hi1 + 2 == lo2:
        a_candidates.add(hi1+1)

b_candidates = set()
for (lo1, hi1), (lo2, hi2) in permutations(ranges_b, r=2):
    if hi1 + 2 == lo2:
        b_candidates.add(hi1+1)

for a, b in product(a_candidates, b_candidates):
    # x + a = b - x
    # 2x = b - a
    # x = (b - a) / 2
    p2x = b - a
    if p2x & 1:  # must have an integer x coordinate
        continue

    px = p2x >> 1

    p = Point(px, px + a)
    for *s, dist in scanners:
        s = Point(*s)

        # check if p is in the range of a scanner
        if abs(s.x - p.x) + abs(s.y - p.y) <= dist:
            break
    else:
        print(p.x, p.y, p.x * 4000000 + p.y)
        break
    
print(perf_counter() - st)