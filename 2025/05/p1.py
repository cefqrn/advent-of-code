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
    a, b = s.split('\n\n')

    ranges = []
    for l in a.splitlines():
        lo, hi = map(int, l.split("-"))
        ranges.append(range(lo, hi+1))
    
    ingredients = []
    for l in b.splitlines():
        ingredients.append(int(l))
    return ranges, ingredients

def solve(data):
    result = 0

    ranges, ingredients = data

    for ingredient in ingredients:
        for r in ranges:
            if ingredient in r:
                result += 1
                break


    return result

if __name__ == "__main__":
    with open("input") as f:
        data = parse(f.read().strip())

    print(solve(data))
