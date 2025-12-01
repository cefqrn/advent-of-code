from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
from heapq import heappop, heappush
from math import inf
from re import findall

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    result = []
    for l in s.splitlines():
        x, k = l[0], int(l[1:])
        result.append((x, k))
    return result

def solve(data):
    dial = 50
    # result = 0

    result = 0
    for x, k in data:
        dial += k * (1 | -(x == "L"))

        result += (dial % 100) == 0




    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
