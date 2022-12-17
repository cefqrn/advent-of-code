from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *
from dataclasses import dataclass
from bisect import insort


@dataclass(frozen=True)
class Valve:
    flow: int
    paths: list[str]
    costs: dict[str, int]
    name: str


valves: dict[str, Valve] = {}
for line in lines:
    _, name, _, _, _, _, _, _, _, *other = line.split()
    flow, *_ = get_ints(line)

    other = [x[:2] for x in other]

    valves[name] = Valve(flow, other, {}, name)

for valve in valves.values():
    others: list[tuple[int, tuple, str]] = [(1, (), path) for path in valve.paths]
    while others:
        cost, history, curr = others.pop(0)

        if curr not in valve.costs and valves[curr].flow:
            valve.costs[curr] = cost
            if len(valve.costs) == len(valves):
                break

        for path in valves[curr].paths:
            if path in history:
                continue

            insort(others, (cost + 1, (*history, curr), path))

possible: list[tuple[int, int, tuple, str, int]] = [(0, 0, ("AA",),"AA", -1)]
# -1 time because "AA" is opened even if it shouldn't be
best = INFINITY_NEGATIVE
best_order = ()

while possible:
    flow_rate, total_flow, opened, curr, minute = possible.pop()

    minute += 1 # time for opening the valve

    total_flow += flow_rate
    flow_rate += valves[curr].flow

    value = total_flow + flow_rate * (30 - minute)
    if value > best:
        best = value
        best_order = opened

    valve = valves[curr]
    for path, cost in valve.costs.items():
        if path in opened:
            continue

        new_time = minute + cost

        if new_time >= 30:
            continue

        possible.append((
            flow_rate,
            total_flow + flow_rate * cost,
            (*opened, path),
            path,
            new_time
        ))
    
print(best, best_order)
