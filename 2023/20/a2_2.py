from collections import defaultdict, deque
from contextlib import suppress
from itertools import count
from pathlib import Path
from math import lcm
from re import match

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

moutputs = {}
mtypes = defaultdict(lambda: None)
minputs = defaultdict(dict)
for line in data.splitlines():
    module, outputs_s = line.split(" -> ")
    mtype, name = match(r"([%&])?(\w+)", module).groups()

    mtypes[name] = mtype

    moutputs[name] = outputs = outputs_s.split(", ")
    for output in outputs:
        minputs[output][name] = False

orders = []
for module in moutputs["broadcaster"]:
    orders.append(order := [])
    remaining = deque([module])
    while remaining:
        current = remaining.popleft()
        if current in order:
            continue
        order.append((current))

        with suppress(KeyError):
            for output in moutputs[current]:
                remaining.append(output)

common = set(order).intersection(*orders[:-1])

mstates = defaultdict(bool)
cycle_lengths = [None] * len(orders)
seen = [set() for _ in orders]
important = list(list(set(order) - common) for order in orders)
for i in count():
    for j, important_modules in enumerate(important):
        if cycle_lengths[j]:
            continue

        state = tuple(mstates[module] for module in important_modules)
        if state in seen[j]:
            cycle_lengths[j] = i
            if all(cycle_lengths):
                print(lcm(*cycle_lengths))
                exit()

        seen[j].add(state)

    current = deque([("broadcaster", False, "button")])
    while current:
        name, pulse, sender = current.popleft()

        try:
            outputs = moutputs[name]
        except KeyError:
            continue

        if (mtype := mtypes[name]) == "%":
            if pulse:
                continue

            mstates[name] = new_pulse = not mstates[name]
        elif mtype == "&":
            minputs[name][sender] = pulse
            new_pulse = not all(minputs[name].values())
        else:
            new_pulse = pulse

        for output in outputs:
            current.append((output, new_pulse, name))
