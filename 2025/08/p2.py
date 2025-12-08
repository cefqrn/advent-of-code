from bisect import bisect_left, bisect_right
from collections import Counter, deque, defaultdict
from fractions import Fraction
from functools import cache, partial
from itertools import chain, cycle, islice, pairwise, combinations, product
from heapq import heappop, heappush
from math import inf, dist, prod
from re import findall, match

from dsu import DisjointSetUnion

directions = (0, 1), (1, 0), (0, -1), (-1, 0)

def parse(s):
    result = []
    for l in s.splitlines():
        result.append(eval(l))


    return result


def solve(data):
    result = 0

    connected = DisjointSetUnion(len(data))

    possible = list(combinations(range(len(data)), 2))
    possible.sort(key=lambda x: dist(data[x[0]], data[x[1]]))

    # print(possible)
    connection_count = 0
    for a, b in possible:
        if connected.union(a, b):
            connection_count += 1
            if connection_count == 999:
                return data[a][0] * data[b][0]
                
                biggest = sorted(map(len, connected.to_sets()))[-3:]
                return prod(biggest)







    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
