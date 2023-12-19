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
remaining = [("in", {"x":(1,4000), "m":(1,4000), "a":(1,4000), "s":(1,4000)})]
while remaining:
    wf, values = remaining.pop()

    if wf.lower() != wf:
        if wf == "A":
            s += prod(b-a+1 for a, b in values.values())
        continue

    current = values
    for rule in workflows[wf][:-1]:
        rule, dest = rule.split(":")

        checked = rule[0]
        if rule[1] == "<":
            num = int(rule[2:])

            lo, hi = values[checked]
            nv0 = values.copy()
            nv0[checked] = (lo, num-1)
            remaining.append((dest, nv0))

            values[checked] = (num, hi)
        elif rule[1] == ">":
            num = int(rule[2:])

            lo, hi = values[checked]
            nv0 = values.copy()
            nv0[checked] = (num+1, hi)
            remaining.append((dest, nv0))

            values[checked] = (lo, num)
        else:
            raise ValueError
    else:
        wf = workflows[wf][-1]

        remaining.append((wf, values))

print(s)
