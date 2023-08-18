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

people = set()
happiness = defaultdict(int)
for l in s.split('\n'):
    person1, _, sign, value, *_, person2 = l.split()
    
    value = int(value)
    if sign == "lose":
        value = -value

    p1, p2 = person1, person2[:-1]
    people.update([p1, p2])
    happiness[(p1, p2)] += value
    happiness[(p2, p1)] += value

def solve(people, happiness):
    b_value = -99999999
    for c in permutations(people):
        v = sum(map(happiness.__getitem__, zip(c, c[1:] + c[:1])))

        if v > b_value:
            b_value = v

    return b_value

print(f"p1: {solve(people, happiness)}")

people.add("me")
print(f"p2: {solve(people, happiness)}")
