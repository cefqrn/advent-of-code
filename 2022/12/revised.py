import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *


def is_climbable(p, n):
    if n == 'E':
        return p == 'z'
    else:
        return ord(n) <= ord(p) + 1 or p == 'S'


highest_pos = (0, 0)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'E':
            highest_pos = i, j
            break
    else:
        continue
    break

p1 = p2 = INFINITY
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'S':
            path = reconstruct_path(astar(lines, (i, j), highest_pos, SIDES, manhattan, predicate=is_climbable), highest_pos)
            p1 = len(path) - 1  # we need amount of movement, not amount of positions

        if c == 'a':
            path = reconstruct_path(astar(lines, (i, j), highest_pos, SIDES, manhattan, predicate=is_climbable), highest_pos)
            s = len(path) - 1
            if s < p2:
                p2 = s

print(p1)
print(p2)
