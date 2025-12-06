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
    for l in s.splitlines()[:-1]:
        result.append(tuple(map(int, findall(r"\d+", l))))

    result += s.splitlines()[-1].split(),
    print(result)
    # for *l, o in list(zip(*(l for l in s.splitlines()))):
        # print(l)

        # print(l)
        # print(l)
        # if o != " ":
        #     result += eval(o.join(l))





    return result

def solve(data):
    result = 0

    for *x, o in zip(*data):
        result += eval(o.join(map(str,x)))






    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
