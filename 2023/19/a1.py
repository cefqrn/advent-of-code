from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import batched, chain, cycle, count, combinations, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
from operator import eq, gt, lt, ge, le, add, sub, mul
from pathlib import Path
from bisect import bisect, bisect_left, insort, insort_left
from heapq import heappop, heappush
from math import ceil, dist, floor, gcd, inf, lcm, prod, sqrt
from sys import setrecursionlimit
from re import findall, finditer, search

try:
    with (Path(__file__).parent / "input").open() as f:
        data = f.read().rstrip()
except FileNotFoundError as e:
    print(e)
    data = " "

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]

COMPLEX_COORDINATES = False

# NESW URDL
directions = [
     (-1,  0), -1 + 0j,
     ( 0,  1),  0 + 1j,
     ( 1,  0),  1 + 0j,
     ( 0, -1),  0 - 1j
][COMPLEX_COORDINATES::2]

height = len(lines)
width = len(lines[0])

wfs, ratings = blocks

workflows = {}
for line in wfs:
    wf, rules = line.split('{')
    workflows[wf] = rules[:-1].split(',')

s=0
for rating in ratings:
    rating = eval(f"dict({rating[1:-1]})")
    wf = "in"
    while wf.lower() == wf:
        for rule in workflows[wf][:-1]:
            rule, dest = rule.split(":")
            if eval("rating[rule[0]]"+rule[1:]):
                wf = dest
                break
        else:
            wf = workflows[wf][-1]

    if wf == "A":
        s+=sum(rating.values())

print(s)
