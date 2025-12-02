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
    result = []
    for x in s.split(","):
        result.append(tuple(map(int, x.split("-"))))

    return result

def solve(data):
    result = 0
    for a, b in data:
        for n in range(a, b+1):
            n = str(n)
            result += int(n) * bool(match("^()", n))(n == n[:len(n) // 2]*2)

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
