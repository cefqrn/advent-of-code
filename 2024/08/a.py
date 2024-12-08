from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

w, h = len(lines[0]), len(lines)

def is_valid(x, y):
    return 0 <= x < w and 0 <= y < h

from collections import defaultdict

nodes = defaultdict(set)
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '.':
            continue

        nodes[c].add((x, y))

from itertools import combinations

p1 = set()
p2 = set()
for node, nodess in nodes.items():
    for (ax, ay), (bx, by) in combinations(nodess, r=2):
        p2.add((ax, ay))
        p2.add((bx, by))

        dx, dy = bx-ax, by-ay

        nx, ny = ax - dx, ay - dy
        if is_valid(nx, ny):
            p1.add((nx, ny))
        while is_valid(nx, ny):
            p2.add((nx, ny))
            nx -= dx
            ny -= dy

        mx, my = bx + dx, by + dy
        if is_valid(mx, my):
            p1.add((mx, my))
        while is_valid(mx, my):
            p2.add((mx, my))
            mx += dx
            my += dy

print(len(p1))
print(len(p2))
