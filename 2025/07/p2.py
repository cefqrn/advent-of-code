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
    result = {}

    beams = set()
    splitters = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "S":
                beams.add((x, y))
            elif c == "^":
                splitters.add((x, y))

    last = y + 1


    return beams, splitters, last

def solve(data):
    result = 0

    beams, splitters, last = data

    @cache
    def solve(pos):
        x, y = pos
        if y == last:
            return 1

        if pos in splitters:
            return solve((x+1, y)) + solve((x-1, y))
        else:
            return solve((x, y+1))

    return solve(beams.pop())


    # seen = set()
    # while beams:
    #     pos = (x, y) = beams.pop()
    #     if pos in seen:
    #         continue
    #     seen.add(pos)

    #     if y == last:
    #         # result += 1
    #         continue

    #     y += 1

    #     npos = x, y
    #     if npos in splitters:
    #         beams.add((x+1, y))
    #         beams.add((x-1, y))
    #         result += 1
    #     else:
    #         beams.add(npos)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
