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

intersections = 0
possibilities = 1
remaining = [(0, start)]
tiles_seen = set()
while remaining:
    steps, (y, x) = remaining.pop()

    if (y, x) in tiles_seen:
        continue
    tiles_seen.add((y, x))

    path_count = 0
    for dy, dx in directions:
        ny, nx = y+dy, x+dx
        if ny not in range(height) or nx not in range(width):
            continue

        c = lines[ny][nx]
        if c == "#":
            continue

        path_count += 1

        remaining.append((steps+1, (ny, nx)))

    if path_count > 2:
        possibilities *= path_count - 1

print(possibilities)


# not 5878