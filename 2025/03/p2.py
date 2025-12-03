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
        lengths = [hi]
        for lo in bank:
            for i, l in tuple(reversed(tuple(enumerate(lengths)))):
                curr = l * 10 + lo

                if i == len(lengths) - 1:
                    lengths.append(curr)
                elif lengths[i+1] < curr:
                    lengths[i+1] = curr

            if lo > lengths[0]:
                lengths[0] = lo
            if len(lengths) >= 12:
                best = max(best, lengths[11])

        # print(lengths[11])
        print(best)

        result += best

    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
