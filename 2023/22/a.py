from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import chain, cycle, count, combinations, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
from operator import eq, gt, lt, ge, le, ne, add, sub, mul
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


def coordinates3(brick):
    s, e = brick
    return [c for c in product(*map(range, s, map(lambda x: x+1, e)))]


def fall(brick, taken):
    s, e = brick
    while True:
        x, y, z = s
        ns = x, y, z-1

        if z < 1:
            break

        x, y, z = e
        ne = x, y, z-1

        if taken.intersection(coordinates3((ns, ne))):
            break

        brick = s, e = ns, ne

    taken.update(coordinates3(brick))
    return brick


def coordinates2(brick):
    s, e = brick
    return [c for c in product(*map(range, s[:2], map(lambda x: x+1, e[:2])))]


bricks = []
for i, line in enumerate(lines):
    brick = sorted(zip(*3*[map(int, findall(r"-?\d+", line))]), key=lambda x: x[2])
    bricks.append(brick)

bricks.sort(key=lambda x: x[0][2])

taken = set()
bricks = [fall(brick, taken) for brick in bricks]

brick_supports = defaultdict(list)
supported_by = defaultdict(list)
for i, brick in enumerate(bricks):
    support_count = 0
    for j, other in enumerate(bricks[i+1:], i+1):
        if brick[1][2] + 1 != other[0][2]:
            continue

        if set(coordinates2(other)).intersection(coordinates2(brick)):
            brick_supports[brick].append(other)
            supported_by[other].append(brick)

s = 0
for brick in bricks:
    for other in brick_supports[brick]:
        if len(supported_by[other]) < 2:
            break
    else:
        s += 1

print(s)

s = 0
for i, brick in enumerate(bricks):
    new_taken = taken - set(chain.from_iterable(coordinates3(b) for b in bricks[i:]))
    new_bricks = [fall(b, new_taken) for b in bricks[i+1:]]
    s += sum(map(ne, new_bricks, bricks[i+1:]))

print(s)
