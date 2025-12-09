from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product, count
from heapq import heappop, heappush
from math import inf, dist, prod
from re import findall, match

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    result = []

    ints = tuple(map(int, findall(r"-?\d+", s)))

    for line in s.splitlines():
        # ints = tuple(map(int, findall(r"-?\d+", s)))
        result.append(eval(line))




    return result


def is_valid(data, curr):
    i, j = curr

    p, q = data[i], data[j]

    lo_x, hi_x = sorted([p[0], q[0]])
    lo_y, hi_y = sorted([p[1], q[1]])

    for p, q in zip(count(i), count(i+1)):
        p %= len(data)
        q %= len(data)

        if q == i:
            return True

        x1, y1 = data[p]
        x2, y2 = data[q]

        assert (x1 == x2) ^ (y1 == y2)

        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        if x1 == x2:
            x = x1
            for y in range(y1, y2+1):
                if lo_x < x < hi_x and lo_y < y < hi_y:
                    return False
        elif y1 == y2:
            y = y1
            for x in range(x1, x2+1):
                if lo_y < y < hi_y and lo_x < x < hi_x:
                    return False
        else:
            assert False


    # for x in count(i+1):
    #     x %= len(data)
    #     if x == i:
    #         return True

    #     x, y = data[x]
    #     if lo_x < x < hi_x and lo_y < y < hi_y:
    #         return False


def solve(data):
    result = 0

    points = []

    important_x = []
    important_y = []
    # for a, b, c in zip(data, data[1:], data[2:]):

    # print(data)
    for a, b in zip(data, data[1:] + data[:1]):
        print(*a, *b, sep=", ")



    result = -inf

    for i, j in combinations(range(len(data)), 2):
        a, b = data[i], data[j]

        x1, y1 = a
        x2, y2 = b

        area = -~abs(x2 - x1) * -~abs(y2 - y1)
        if area < result:
            continue

        if is_valid(data, (i, j)):
            print(a, b, area)
            result = max(area, result)


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
