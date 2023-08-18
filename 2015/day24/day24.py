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

from itertools import combinations
from functools import reduce, partial

def get_valid(nums, count):
    target = sum(nums) // count

    if count == 1:
        return nums

    for c in range(len(nums)):
        for combination in combinations(nums, r=c):
            if sum(combination) != target:
                continue

            if get_valid(set(nums) - set(combination), count - 1):
                return combination
    
    return tuple()

nums = tuple(map(int, s.splitlines()))
quantum_entanglement = partial(reduce, int.__mul__)

print(f"p1: {quantum_entanglement(get_valid(nums, 3))}")
print(f"p2: {quantum_entanglement(get_valid(nums, 4))}")
