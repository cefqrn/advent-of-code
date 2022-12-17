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
    paths: tuple[str]
    costs: dict[str, int]
    name: str


valves: dict[str, Valve] = {}
valves_wf_count = 0
for line in lines:
    _, name, _, _, _, _, _, _, _, *other = line.split()
    flow, *_ = get_ints(line)

    valves_wf_count += flow > 0

    valves[name] = Valve(flow, tuple(x[:2] for x in other), {}, name)


for valve in valves.values():
    others: list[tuple[int, tuple, str]] = [(1, (), path) for path in valve.paths]
    while others:
        cost, history, curr = others.pop(0)
        curr_v = valves[curr]

        if curr not in valve.costs and curr_v.flow:
            valve.costs[curr] = cost
            if len(valve.costs) == valves_wf_count:
                break

        for path in curr_v.paths:
            if path in history:
                continue

            insort(others, (cost + 1, (*history, curr), path))


print(valves_wf_count)

possible: list[tuple[int, int, tuple, str, int]] = [(0, 0, ("AA",), "AA", -1)]
possible_paths = []
while possible:
    flow_rate, total_flow, opened, curr, time = possible.pop()

    total_flow += flow_rate
    flow_rate += valves[curr].flow

    time += 1 # time for opening the valve

    value = total_flow + flow_rate * (26 - time)
    insort(possible_paths, (value, opened))

    valve = valves[curr]
    for path, cost in valve.costs.items():
        if path in opened:
            continue

        new_time = time + cost

        if new_time >= 26:
            continue

        possible.append((
            flow_rate,
            total_flow + flow_rate * cost,
            (*opened, path),
            path,
            new_time
        ))
    
print(possible_paths[-1])

best = INFINITY_NEGATIVE
best_order = ()
for start_flow, already_opened in possible_paths:
    possible: list[tuple[int, int, tuple, str, int]] = [(0, start_flow, already_opened, "AA", -1)]
    while possible:
        flow_rate, total_flow, opened, curr, time = possible.pop()

        total_flow += flow_rate
        flow_rate += valves[curr].flow

        time += 1 # time for opening the valve

        value = total_flow + flow_rate * (26 - time)
        if value > best:
            best = value
            best_order = opened
            print(best, best_order)

        valve = valves[curr]
        for path, cost in valve.costs.items():
            if path in opened:
                continue

            new_time = time + cost

            if new_time >= 26:
                continue

            possible.append((
                flow_rate,
                total_flow + flow_rate * cost,
                (*opened, path),
                path,
                new_time
            ))
