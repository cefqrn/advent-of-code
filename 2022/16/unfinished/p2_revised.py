from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *
from collections import defaultdict
from itertools import product
from bisect import insort


paths: dict[str, dict[str, int]] = defaultdict(dict)
flows: dict[str, int] = {}
valves_wflow: set[str] = set()
for line in lines:
    _, valve, _, _, flow_s, _, _, _, _, *tunnels = line.split()
    flow = int(flow_s[5:-1])

    for tunnel in tunnels:
        paths[valve][tunnel[:2]] = 1

    flows[valve] = flow

    if flow:
        valves_wflow.add(valve)

i=0
for start, destination in product(valves_wflow, valves_wflow):
    if destination in paths[start]:
        continue
    neighbors: deque[tuple[int, str]] = deque((cost, path) for path, cost in paths[start].items())
    while neighbors:
        cost, current = neighbors.popleft()

        paths[start].setdefault(current, cost)
        paths[current].setdefault(start, cost)
        
        for path, path_cost in paths[current].items():
            if path in paths[start] or path == start:
                continue

            insort(neighbors, (cost+path_cost, path))


possible: list[tuple[tuple[str, ...], int, int]] = [(("AA",), -1, 0)]
combinations = {}
while possible:
    visited, time, total_released = possible.pop()
    curr = visited[-1]

    for valve in valves_wflow:
        if valve in visited:
            continue

        cost = paths[curr][valve]

        new_time = time + cost + 1
        if new_time > 26:
            continue

        new_total = total_released + (26-new_time-1)*flows[valve]

        new_visited = *visited, valve

        combinations[new_visited] = new_total
        possible.append((new_visited, new_time, new_total))

print(len(combinations))
print(i)