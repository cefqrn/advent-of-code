from collections import defaultdict
from functools import partial
from operator import ge
from heapq import heappop, heappush
from math import inf

def is_wall(x, y):
    value = x*x + 3*x + 2*x*y + y + y*y + number
    return value.bit_count() & 1

def h(x, y):
    return abs(target[0] - x) + abs(target[1] - y)

def iter_len(i):
    return sum(1 for _ in i)

number = 1358
target = 31,39

p1 = None

p = 1, 1
costs = defaultdict(lambda: inf)
possibilities = [(h(*p), 0, p)]
while possibilities:
    _, cost, p = heappop(possibilities)
    x, y = p

    if p == target:
        p1 = cost

    if p1 is not None and cost >= 50:
        continue

    ncost = cost + 1
    for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
        np = nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or is_wall(nx, ny):
            continue

        if costs[np] < ncost: continue
        costs[np] = ncost

        heappush(possibilities, (h(nx, ny) + ncost, ncost, np))

print(p1, iter_len(filter(partial(ge, 50), costs.values())))
