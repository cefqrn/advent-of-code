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

modules = {}
states = {}
inputs = defaultdict(dict)
for line in lines:
    name, outputs = line.split(" -> ")
    btype, name = name[0], name[1:]

    outputs = outputs.split(", ")

    modules[name] = btype, outputs
    states[name] = 0
    for output in outputs:
        inputs[output][name] = 0

pulses = [0, 0]
for _ in range(1000):
    current = [("roadcaster", 0, "button")]
    while current:
        name, pulse, sender = current.pop(0)
        pulses[pulse] += 1

        try:
            btype, outputs = modules[name]
        except KeyError:
            continue

        if btype == "b":
            new_pulse = pulse
        elif btype == "%":
            if pulse:
                continue

            states[name] = new_pulse = not states[name]
        elif btype == "&":
            inputs[name][sender] = pulse
            new_pulse = not all(inputs[name].values())

        for output in outputs:
            current.append((output, new_pulse, name))

lo, hi = pulses
print(lo*hi)
