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
        # ints = tuple(map(int, findall(r"-?\d+", s)))
        result.append(eval(line))




    return result


def solve(data):
    result = 0

    for a, b in combinations(data, 2):

        print(a, b)
        x1, y1 = a
        x2, y2 = b

        area = -~abs(x2-x1) * -~abs(y2 - y1)
        result = max(area, result)




    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
