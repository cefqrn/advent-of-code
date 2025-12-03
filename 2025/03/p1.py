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
    for x in s.splitlines():
        result.append(tuple(map(int, x)))

    return result

def solve(data):
    result = 0
    for bank in data:
        best = 0
        hi, *bank = bank
        for lo in bank:
            curr = hi*10 + lo
            hi = max(hi, lo)
            best = max(best, curr)

        result += best

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
