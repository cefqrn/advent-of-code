from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import  chain, cycle, count, combinations, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
from operator import eq, gt, lt, ge, le, add, sub, mul, neg
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
end = (height-1, width-2)
nodes = {start, end}

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if lines[y][x] == "#":
            continue

        options = 0
        for dy, dx in directions:
            np = ny, nx = y+dy, x+dx

            if ny not in range(height) or nx not in range(width):
                continue

            c = lines[ny][nx]
            if c == "#":
                continue

            options += 1

        if options > 2:
            nodes.add((y, x))

edges = defaultdict(dict)
for node in nodes:
    seen = {node}
    remaining = [(0, node)]
    while remaining:
        steps, (y, x) = remaining.pop()

        nsteps = steps + 1
        for dy, dx in directions:
            npos = ny, nx = y+dy, x+dx

            if ny not in range(height) or nx not in range(width):
                continue

            c = lines[ny][nx]
            if c == "#":
                continue

            if npos in seen:
                continue
            seen.add(npos)

            if npos in nodes:
                edges[node][npos] = nsteps
                edges[npos][node] = nsteps
                continue

            remaining.append((nsteps, npos))

remaining = [(0, start, set())]
best = 0
while remaining:
    steps, node, seen = remaining.pop()

    if node == end:
        if best < steps:
            best = steps

        continue

    for adjacent, cost in edges[node].items():
        if adjacent in seen:
            continue

        remaining.append((steps+cost, adjacent, seen | {node}))

print(best)
