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

def h(y, x):
    return -(abs(height-1 - y) + abs(width-2 - x))


seen = defaultdict(int)

remaining = [(h(*start), 0, start, {})]
while remaining:
    steps, (y, x), tiles_seen = heappop(remaining)

    for dy, dx in directions:
        ny, nx = y+dy, x+dx
        if ny not in range(height) or nx not in range(width):
            continue

        if (ny, nx) in tiles_seen:
            continue

        c = lines[ny][nx]
        if c == "#":
            continue

        heappush(remaining, (steps+h(ny, nx), steps-1, (ny, nx), {(ny, nx), *tiles_seen}))


print(max(hikes))


# not 5878