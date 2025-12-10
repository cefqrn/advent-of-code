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

from itertools import compress, count

def solve(data):
    result = 0

    for i, (_, b, c) in enumerate(data):
        left = [(0, tuple(eval(c[1:-1])), tuple(sorted(b, key=len, reverse=True)))]

        seen = defaultdict(lambda: inf)
        while left:
            cost, amounts, buttons_left = heappop(left)

            print(amounts, cost)

            state = amounts, buttons_left
            if seen[state] <= cost:
                continue
            seen[state] = cost


            if not any(amounts):
                best = cost
                break

            if not buttons_left:
                continue

            x = buttons_left[0]
            rest = buttons_left[1:]

            # solve without
            heappush(left, (cost, amounts, rest))

            na = list(amounts)
            for i in x:
                na[i] -= 1
                if na[i] < 0:
                    break
            else:
                heappush(left, (cost+1, tuple(na), buttons_left))

        # left = []
        result += best

        print(i, best)

        # break


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
