from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

from collections import defaultdict
from itertools import permutations

z = lambda: defaultdict(int)
happiness = defaultdict(z)
for l in s.split('\n'):
    person1, _, sign, value, *_, person2 = l.split()
    
    value = int(value)
    if sign == "lose":
        value = -value

    happiness[person1][person2[:-1]] = value

def solve(happiness):
    b_value = -99999999
    for c in permutations(happiness):
        v = 0
        for p1, p2 in zip(c, [*c[1:], c[0]]):
            v += happiness[p1][p2] + happiness[p2][p1]

        if v > b_value:
            b_value = v

    return b_value

print(f"p1: {solve(happiness)}")

happiness["me"]
print(f"p2: {solve(happiness)}")
