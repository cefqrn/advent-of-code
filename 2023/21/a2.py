from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from fractions import Fraction
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

n = 26501365
start_max = n % height

values = []
for i in range(3):
    max_step = start_max + i * height
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

    values.append(len(visitable[max_step & 1]))

def f(x):
    a = Fraction(values[2] + values[0] - 2*values[1], (start_max + 2*height)**2 + (start_max)**2 - 2*(start_max + height)**2)
    b = Fraction(values[2] - values[0] - a * ((start_max + 2*height)**2 - start_max**2), 2*height)
    c = values[0] - b * start_max - a * start_max**2

    return a*x**2 + b*x + c

print(f(n))

"""
x = start_max
y = height

a * (x + 0y)**2 + b * (x + 0y) + c = values[0]
a * (x + 1y)**2 + b * (x + 1y) + c = values[1]
a * (x + 2y)**2 + b * (x + 2y) + c = values[2]

a((x + 1y)**2 - (x + 0y)**2) + b(x + 1y - (x + 0y)) = values[1] - values[0]
a((x + 2y)**2 - (x + 0y)**2) + b(x + 2y - (x + 0y)) = values[2] - values[0]

a * 2((x + 1y)**2 - (x + 0y)**2) + b * 2y = 2(values[1] - values[0])
a *  ((x + 2y)**2 - (x + 0y)**2) + b * 2y =   values[2] - values[0]

a*((x + 2y)**2 - (x + 0y)**2 - 2((x + 1y)**2 - (x + 0y)**2)) = values[2] - values[0] - 2(values[1] - values[0])

a*((x + 2y)**2 + (x + 0y)**2 - 2*(x + 1y)**2) = values[2] + values[0] - 2*values[1]

a = Fraction(values[2] + values[0] - 2*values[1], (x + 2y)**2 + x**2 - 2*(x + 1y)**2)

a * ((x + 2y)**2 - (x + 0y)**2) + b * 2y = values[2] - values[0]
b = Fraction(values[2] - values[0] - a * ((x + 2y)**2 - (x + 0y)**2), 2y)

a * (x + 0y)**2 + b * (x + 0y) + c = values[0]
c = values[0] - b * (x + 0y) - a * (x + 0y)**2
"""