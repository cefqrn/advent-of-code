from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import batched, chain, cycle, count, combinations, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
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

spots = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        spots[y, x] = c
        if c == "S":
            start = y, x

max_step = 64

remaining = [(0, *start)]
seen = defaultdict(lambda: inf)
visitable = [set(), set()]
while remaining:
    state = step, y, x = heappop(remaining)

    if (c := spots[y % height, x % width]) == "#":
        continue

    if c in ".S":
        visitable[step & 1].add((y, x))

    if step == max_step:
        continue

    if seen[y, x] <= step:
        continue
    seen[y, x] = step

    for dy, dx in directions:
        heappush(remaining, (step+1, y+dy, x+dx))

print(len(visitable[max_step & 1]))
