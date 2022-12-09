import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *
from itertools import pairwise

coords = [[0, 0] for _ in range(10)]
def move():
    global coords
    i = 0
    for h, t in pairwise(coords):
        i += 1
        while (abs(hd := h[0] - t[0]) > 1) or (abs(h[1] - t[1]) > 1):
            vd = h[1] - t[1]
            # print(t[0], t[1])
            if hd and vd:
                t[0] += hd // abs(hd)
                t[1] += vd // abs(vd)
                if i == 9:visited.add((t[0], t[1]))
                continue

            if hd:
                t[0] += hd // abs(hd)
                if i == 9:visited.add((t[0], t[1]))
                continue

            if vd:
                t[1] += vd // abs(vd)
                if i == 9:visited.add((t[0], t[1]))

visited: set[tuple[int, int]] = set([(0, 0),])
for line in lines:
    match line.split():
        case ["L", n]:
            for _ in range(int(n)):
                coords[0][0] -= 1
                move()

        case ["R", n]:
            for _ in range(int(n)):
                coords[0][0] += 1
                move()

        case ["U", n]:
            for _ in range(int(n)):
                coords[0][1] += 1
                move()

        case ["D", n]:
            for _ in range(int(n)):
                coords[0][1] -= 1
                move()

print(len(visited))
