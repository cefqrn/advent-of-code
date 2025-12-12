from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
from heapq import heappop, heappush
from math import inf, dist, prod
from re import compile, findall, match

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

INT = compile(r"-\d+?")

def parse(s):
    result = []

    *a, b = s.split("\n\n")
    # *a, b = s.split()
    # b = b.splitlines()

    shapes = []
    for x in a:
        shapes.append(x.splitlines()[1:])

    regions = []
    for x in b.splitlines():
        d, amounts = x.split(": ")
        w, h = map(int, d.split("x"))
        amounts = tuple(map(int, amounts.split()))

        regions.append(((w, h), amounts))


        # b.split


    return shapes, regions

def solve(data):
    result = 0

    shapes, regions = data

    left = 0
    for region in regions:
        (w, h), amounts = region

        base = (w//3) * (h//3)

        if sum(amounts) <= base:
            result += 1
        else:
            left += 1

        # print((w//3) * (h//3), sum(amounts))
        # print()

    # print(left)

        # asdf = 0
        # for amount in amounts:
        #     print(amount)


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
