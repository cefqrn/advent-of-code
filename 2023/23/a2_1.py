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


seen = defaultdict(int)

setrecursionlimit(9**9)

@cache
def longest_path(start, end, direction, banned):
    if start == end:
        return 0

    possibilities = []
    remaining = [(0, start, direction)]
    while remaining:
        steps, (y, x), direction = remaining.pop()

        options = 0
        for new_direction in directions:
            if (directions.index(new_direction) - 2) % 4 == directions.index(direction):
                continue

            dy, dx = new_direction
            new_start = ny, nx = y+dy, x+dx

            if new_start == end:
                return steps+1

            if new_start in banned:
                continue

            if ny not in range(height) or nx not in range(width):
                continue

            c = lines[ny][nx]
            if c == "#":
                continue

            options += 1
            remaining.append((steps+1, new_start, new_direction))

        if options > 1:
            possibilities.extend(remaining[-options:])
            remaining = remaining[:-options]

    longest = 0
    for steps, new_start, new_direction in possibilities:
        result = steps + longest_path(new_start, end, new_direction, banned | {tuple(map(sub, new_start, new_direction))})
        longest = max(longest, result)

    return longest

print(longest_path(start, (height - 1, width - 2), directions[2], frozenset()))
# print(longest_path(start, (5,3), directions[2], frozenset()))
