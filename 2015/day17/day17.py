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

volume = 150

def solve(containers, max_depth=-1):
    possibilities = set((value, 0, frozenset(((value, i),))) for value, i in containers)
    solutions = set()

    while possibilities:
        s, depth, possibility = possibilities.pop()

        if depth + 1 == max_depth:
            continue

        for container in containers:
            if container in possibility:
                continue

            value, _ = container
            new_s = s + value

            new_possibility = (new_s, depth + 1, possibility | {container})
            
            if new_s < volume:
                possibilities.add(new_possibility)
            elif new_s == volume:
                solutions.add(new_possibility)
    
    return solutions


containers: tuple[tuple[int, int]] = *((value, i) for i, value in enumerate(eval(s.replace('\n', ',')))),
solutions = solve(containers)

print(f"p1: {len(solutions)}")
c = len(min(solutions, key=lambda x: len(x[2]))[2])

print(f"p2: {len(solve(containers, c))}")