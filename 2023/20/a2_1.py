# does not work

from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import chain, cycle, count, combinations, filterfalse, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
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


def get_parents(module, seen=None):
    if seen is None:
        seen = set()
    elif module in seen:
        return seen
    else:
        seen.add(module)

    for inp in inputs[module]:
        get_parents(inp, seen)

    return seen


non_recursive = [module for module in modules if module not in get_parents(module)]

states_seen = [[0] * len(non_recursive)]
changes_seen = []
for i in count(1):
    current_changes = []
    remaining = [("roadcaster", 0, "button")]
    while remaining:
        name, pulse, sender = remaining.pop(0)

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
            remaining.append((output, new_pulse, name))
            current_changes.append((output, new_pulse, name))

    current_state = [states[module] for module in non_recursive]
    if current_state in states_seen:
        cycle_start = states_seen.index(current_state)
        cycle_length = i - cycle_start
        break
    states_seen.append(current_state)
    changes_seen.append(current_changes)

print(cycle_start, cycle_length)

print(*changes_seen[cycle_start:], sep='\n')
print()

ignoring = [
    [change for change in changes if change[-1] not in non_recursive]
    for changes in changes_seen[cycle_start:]
]

print(*ignoring, sep='\n')
