from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
from heapq import heappop, heappush
from math import inf
from re import findall, match

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    grid = {}
    for y, l in enumerate(s.splitlines()):
        for x, c in enumerate(l):
            grid[x, y] = c

    return grid

def solve(data):
    result = 0

    NEIGHBORS = tuple(product(range(-1, 1+1), repeat=2))

    to_update = set(data)
    while to_update:
        coords = x, y = to_update.pop()

        c = data.get(coords)

        if c != "@":
            continue

        neighbor_count = 0
        for dx, dy in NEIGHBORS:

            if dx == dy == 0:
                continue

            nx, ny = x+dx, y+dy
            if data.get((nx, ny)) == "@":
                neighbor_count += 1

        if neighbor_count < 4:
            data[(x, y)] = "."
            result += 1

            for dx, dy in NEIGHBORS:
                nx, ny = x+dx, y+dy


                to_update.add((nx,ny))





    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
