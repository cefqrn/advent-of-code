from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from bisect import insort
from re import findall

SEARCH_AREA = 20


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __floordiv__(self, other: int):
        return Point(self.x // other, self.y // other)

    def __iter__(self):
        return iter([self.x, self.y])

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


lines_a: list[tuple[Point, Point]] = []  # like /
lines_b: list[tuple[Point, Point]] = []  # like \

intersections: set[Point] = set()
scanners = []
with open(0) as f:
    for i, line in enumerate(f.readlines()):
        x, y, bx, by = map(int, findall(r"[-+]?\d+", line))
        dist = abs(x-bx) + abs(y-by)

        a, b, c, d = diamond = (
            Point(x, y+dist),
            Point(x+dist, y),
            Point(x, y-dist),
            Point(x-dist, y)
        )

        scanners.append((x, y, dist))

        lines_a.extend([(c, b), (d, a)])
        lines_b.extend([(a, b), (d, c)])

        intersections.update(diamond)

# find other intersections
for l1, l2 in product(lines_a, lines_b):
    a, b = l1
    c, d = l2

    # slopes are 1 and -1, solve lines for x
    two_x = a.x - a.y + c.x + c.y
    x = two_x >> 1

    # point must be in the middle of 4 integer coordinates
    if two_x & 1:
        continue

    # intersection must be on both lines
    if x > min(b.x, d.x) or x < max(a.x, c.x):
        continue

    y = (x - a.x) + a.y
    
    intersections.add(Point(x, y))

# find a 2 across, 2 tall diamond whose center is not in a diamond
intersections_list = list(intersections)
for i, p1 in enumerate(intersections_list):
    x1, y1 = p1

    closest = []
    for p2 in intersections_list[i:]:
        x2, y2 = p2

        if abs(x1 - x2) + abs(y1 - y2) != 2:
            continue

        closest.append(p2)

    if len(closest) == 3:
        x, y = sum(closest, start=p1) // 4

        ranges = []
        for px, py, d in scanners:
            if (dh:=abs(py-y)) > d:
                continue

            insort(ranges, (px - (d - dh), px + (d - dh)))

        ranges = combine_ranges(ranges)

        for lo, hi in ranges:
            if lo < x <= hi:
                break
        else:
            print(x*4000000 + y)
            break
