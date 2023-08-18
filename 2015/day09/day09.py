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

# s is the input as a string

from collections import defaultdict, namedtuple
from bisect import insort

Path = namedtuple("Path", ["visited", "location", "dist"])
Edge = namedtuple("Edge", ["dest", "dist"])

locations = set()
edges = defaultdict(list)
for l in s.strip().split('\n'):
    p1, _, p2, _, dist = l.split()
    
    locations.update((p1, p2))
    dist = int(dist)

    edges[p1].append(Edge(p2, dist))
    edges[p2].append(Edge(p1, dist))

paths = [Path({start}, start, 0) for start in locations]
distances: list[int] = []
while paths:
    visited, curr, curr_dist = path = paths.pop()

    if len(visited) == len(locations):
        insort(distances, curr_dist)
        continue

    for dest, dist in filter(lambda x: x.dest not in visited, edges[curr]):
        paths.append(Path({*visited, dest}, dest, curr_dist + dist))

print(f'p1: {distances[0]}')
print(f'p2: {distances[-1]}')
