import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoc_library import *

from dataclasses import dataclass

@dataclass
class Monkey:
    items: list
    operation: str
    test: int
    target_true: int
    target_false: int
    inspections: int

monkeys: list[Monkey] = []

for block in blocks:
    lines = block.split('\n')
    monkey = Monkey(
        items = get_ints(' '.join(lines[1].split()[2:])),
        operation = ' '.join(lines[2].split()[1:]),
        test = int(lines[3].split()[-1]),
        target_true = int(lines[4].split()[-1]),
        target_false = int(lines[5].split()[-1]),
        inspections=0
    )

    monkeys.append(monkey)

for _ in range(20):
    for monkey in monkeys:
        for item in monkey.items:
            monkey.inspections += 1

            old = item

            new = old
            exec(monkey.operation)

            new //= 3

            if new % monkey.test == 0:
                monkeys[monkey.target_true].items.append(new)
            else:
                monkeys[monkey.target_false].items.append(new)

        monkey.items = []
        
inspections = [monkey.inspections for monkey in monkeys]
inspections.sort()

print(inspections.pop() * inspections.pop())
