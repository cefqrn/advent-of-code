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


from itertools import compress
def solve(data):
    result = 0

    # @cache
    # def solve(n):

    for a, b, _ in data:
        best = inf
        for p in product((False, True), repeat=len(b)):
            if sum(p) >= best:
                continue

            na = [0] * len(a)
            for indices in compress(b, p):
                print(indices)
                for x in indices:
                    na[x] ^= 1

            print(na, a, p)
            if na == list(a):
                best = sum(p)

        result += best

        # break


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().rstrip("\n"))

    print(solve(data))
