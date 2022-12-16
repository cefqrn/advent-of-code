# this one isn't done but is kept for its Point class

from __future__ import annotations

from dataclasses import dataclass
from bisect import insort
from math import radians, sin, cos
from time import perf_counter
from re import findall

from typing import Optional

st = perf_counter()

SEARCH_WIDTH = 20
EPSILON = .01


@dataclass(frozen=True, order=True, slots=True)
class Point:
    x: float
    y: float

    def rotated(self, angle_deg: float, pivot: Optional[Point]=None) -> Point:
        if pivot is None:
            pivot = Point(0, 0)

        px, py = pivot

        x, y = self.x - px, self.y - py

        angle_rad = radians(angle_deg)

        s = sin(angle_rad)
        c = cos(angle_rad)

        x, y = c*x - s*y,  s*x + c*y

        return Point(x + px, y + py)

    def __iter__(self):
        return iter([self.x, self.y])
    
    def __getitem__(self, i):
        return [self.x, self.y][i]

    def __repr__(self):
        return f"({self.x:+.02f}, {self.y:+.02f})"


def combine_ranges(ranges):
    new_ranges = []

    prev = ranges[0]
    for curr in ranges[1:]:
        if prev[1] < curr[0] - EPSILON:
            new_ranges.append(prev)
            prev = curr
            continue

        prev = (prev[0], max(prev[1], curr[1]))
    
    if not new_ranges or new_ranges[-1] != prev:
        new_ranges.append(prev)
    
    return new_ranges


pivot = Point(SEARCH_WIDTH/2, SEARCH_WIDTH/2)

lengths = []
heights = []
intersections = []
with open(0) as f:
    for i, line in enumerate(f.readlines()):
        x, y, bx, by = map(float, findall(r"[-+]?\d+", line))
        dist = abs(x-bx) + abs(y-by)

        hi_x, hi_y = Point(x, y+dist).rotated(-45, pivot)
        lo_x, lo_y = Point(x, y-dist).rotated(-45, pivot)

        lo_x, lo_y = max(lo_x, 0), max(lo_y, 0)
        hi_x, hi_y = min(hi_x, SEARCH_WIDTH), min(hi_y, SEARCH_WIDTH)

        insort(lengths, (lo_x, hi_x))
        insort(heights, (lo_y, hi_y))


print(lengths)
print(heights)

lengths = combine_ranges(lengths)
heights = combine_ranges(heights)

print(lengths)
print(heights)