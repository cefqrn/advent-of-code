from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import  chain, cycle, count, combinations, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
from operator import eq, gt, lt, ge, le, add, sub, mul
from pathlib import Path
from bisect import bisect, bisect_left, insort, insort_left
from heapq import heappop, heappush
from math import ceil, dist, floor, gcd, inf, lcm, prod, sqrt
from sys import setrecursionlimit
from re import findall, finditer, search

try:
    with (Path(__file__).parent / "input").open() as f:
        data = f.read().rstrip()
except FileNotFoundError as e:
    print(e)
    data = " "

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]

COMPLEX_COORDINATES = False

# NESW URDL
directions = [
     (-1,  0), -1 + 0j,
     ( 0,  1),  0 + 1j,
     ( 1,  0),  1 + 0j,
     ( 0, -1),  0 - 1j
][COMPLEX_COORDINATES::2]

height = len(lines)
width = len(lines[0])

start = (0, 1)

hikes = []

seen = defaultdict(lambda: -1)
remaining = [(0, start, frozenset({(0, 1)}))]
while remaining:
    steps, (y, x), tiles_seen = remaining.pop()

    if seen[tiles_seen] >= steps:
        continue
    seen[tiles_seen] = steps

    if (y, x) == (height-1, width-2):
        hikes.append(steps)
        continue

    for dy, dx in directions:
        ny, nx = y+dy, x+dx
        if ny not in range(height) or nx not in range(width):
            continue

        c = lines[ny][nx]
        if c == "#":
            continue

        if (ny, nx) in tiles_seen:
            continue

        remaining.append((steps+1, (ny, nx), tiles_seen | {(ny, nx)}))

print(max(hikes))
