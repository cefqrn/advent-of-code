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

from copy import deepcopy

NEIGHBORS = [(a, b) for a in range(-1, 2) for b in range(-1, 2) if a or b]


def iterate(rows):
    new_rows = []

    for y, row in enumerate(rows):
        new_rows.append([])
        for x, _ in enumerate(row):
            n_count = 0
            for dx, dy in NEIGHBORS:
                nx = x + dx
                ny = y + dy

                if x + dx < 0 or len(row) <= x + dx or y + dy < 0 or len(rows) <= y + dy:
                    continue

                n_count += rows[ny][nx]
            
            if n_count == 3:
                new_rows[-1].append(1)
            elif n_count != 2:
                new_rows[-1].append(0)
            else:
                new_rows[-1].append(rows[y][x])
    
    return new_rows
    

p1_rows = list(map(lambda row: list(map("#".__eq__, row)), s.splitlines()))

w, h = len(p1_rows[0]), len(p1_rows)
corners = [(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)]

p2_rows = deepcopy(p1_rows)
for x, y in corners:
    p2_rows[y][x] = 1

for _ in range(100):
    p1_rows = iterate(p1_rows)
    p2_rows = iterate(p2_rows)
   
    for x, y in corners:
        p2_rows[y][x] = 1

print(f"p1: {sum(map(sum, p1_rows))}")
print(f"p2: {sum(map(sum, p2_rows))}")
