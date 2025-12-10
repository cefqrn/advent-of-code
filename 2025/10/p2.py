# see p2_7.py for first working solution

from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
from heapq import heappop, heappush
from math import inf, dist, prod
from re import findall, match

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    result = []

    ints = tuple(map(int, findall(r"-?\d+", s)))

    for line in s.splitlines():
        a, *b, c = line.split()

        a = tuple(map(".#".find, a))


        b = tuple(tuple(map(int, findall(r"-?\d+", k))) for k in b)
        result.append((a[1:-1], b, c))




    return result


from contextlib import contextmanager

@contextmanager
def removed(amount, buttons):
    for i in buttons:
        amount[i] -= 1

    try:
        yield
    finally:
        for i in buttons:
            amount[i] += 1

from itertools import compress
def solve(data):
    result = 0

    @cache
    def solve(left, i, buttons):
        na = list(left)
        best = inf
        for x in buttons:
            with removed(na, x):
                if any(k < 0 for k in na):
                    continue

                if not any(na):
                    return 1

                best = min(best, solve(tuple(na), buttons))
        return 1 + best
            




    for _, b, c in data:
        best = solve(tuple(eval(c[1:-1])), b)

        # left = []
        result += best

        # break


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
