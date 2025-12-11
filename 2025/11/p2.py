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

    connections = defaultdict(set)
    for line in s.splitlines():
        a, b = line.split(": ")
        b = b.split()

        for x in b:
            connections[a].add(x)


    return connections

def solve(connections):
    result = 0

    @cache
    def num_paths(source, target):
        if source == target:
            return 1

        result = 0
        for x in connections[source]:
            result += num_paths(x, target)

        return result


    a = num_paths("svr", "dac")
    b = num_paths("dac", "fft")
    c = num_paths("fft", "out")

    result += a*b*c

    a = num_paths("svr", "fft")
    b = num_paths("fft", "dac")
    c = num_paths("dac", "out")

    result += a*b*c


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
