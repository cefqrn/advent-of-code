# does not work

from collections import Counter, defaultdict, deque
from contextlib import suppress
from functools import cache, partial
from itertools import batched, chain, cycle, compress, combinations, count, groupby, islice, pairwise, permutations, product, repeat, starmap, tee
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

modules["rx"] = None, ()


def weave(iterable, yield_indices=False):
    iters = list(map(iter, iterable))
    previous = list(map(next, iters))

    if yield_indices:
        while True:
            yield (lowest := min(previous), lowest_index := previous.index(lowest))
            previous[lowest_index] = next(iters[lowest_index])
    else:
        while True:
            yield (lowest := min(previous))
            previous[lowest_index] = next(iters[lowest_index := previous.index(lowest)])


def last_value(iterable):
    return deque(iterable, maxlen=1)[0]


AAA = 0
def button_count(name, pulse, path=None):
    """
    yields the amount of times the button needs to be pressed
    for the module to output the required pulse
    """

    global AAA
    print(AAA:=AAA+1, name, pulse)

    if path is None:
        path = set()

    if name in path:
        yield 1

    btype, _ = modules[name]

    if name == "rx":
        yield from weave(button_count(inp, pulse) for inp in inputs[name])
    elif btype == "b":
        yield from count(1)
    elif btype == "%":
        if pulse:
            yield from islice(weave(button_count(inp, 0, {name, *path}) for inp in inputs[name]), 0, None, 2)
        else:
            yield from islice(weave(button_count(inp, 0, {name, *path}) for inp in inputs[name]), 1, None, 2)
    elif btype == "&":
        if len(inputs[name]) == 1:
            yield from button_count([*inputs[name].keys()][0], not pulse, {name, *path})

        enabled = [0] * len(inputs[name])
        for v, g in groupby(
            weave((weave((button_count(inp, 0), button_count(inp, 1)), yield_indices=True) for inp in inputs[name]), yield_indices=True),
            key=lambda x: x[0][1]
        ):
            (flip_count, _), module_index = last_value(g)
            enabled[module_index] = v

            if not all(enabled) == pulse:
                yield flip_count

    raise ValueError


print(next(button_count("rx", False)))

# rx
# any of its inputs need to send a low pulse
# ignores high pulses

# broadcast
# 1

# %
# needs to receive two low pulses
# ignores high pulses

# &
# needs to **remember** a high pulse for all its inputs
# otherwise sends a high pulse