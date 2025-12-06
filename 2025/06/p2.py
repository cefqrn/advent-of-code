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
    result = 0
    # for l in 
    # print(s.splitlines()[0])
    # for l in s.splitlines():
        # print(l)
    result = []
    lines = s.splitlines()


    indices = []
    for i, x in enumerate(lines[-1]):
        if not x.isspace():
            indices.append(i)

    indices.append(i + 2)

    print(indices)

    result = []
    for a, b in pairwise(indices):

        strs = []
        for l in lines[:-1]:
            strs.append(l[a:b-1])
        result.append([int("".join(n)) for n in zip(*strs)])

    return result, [lines[-1][i] for i in indices[:-1]]

def solve(data):
    result = 0

    print(data)


    data, ops = data
    print(data, ops)

    for x, o in zip(data, ops):
        print(o)
        result += eval(o.join(map(str,x)))






    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read())

    print(solve(data))
