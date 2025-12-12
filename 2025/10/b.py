# https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

from functools import cache
from itertools import chain, combinations
from math import inf

@cache
def light_configuration_possibilities(diagram, buttons):
    result = []
    for push_count in range(min(len(diagram), len(buttons))+1):
        for buttons_pushed in combinations(buttons, push_count):
            lights = list(diagram)
            for button in buttons_pushed:
                for i in button:
                    lights[i] ^= 1

            if not any(lights):
                result.append(buttons_pushed)

    return result

@cache
def joltage_configuration_cost(joltages, buttons):
    if not any(joltages):
        return 0

    bits = tuple(joltage & 1 for joltage in joltages)

    best = inf
    for buttons_pushed in light_configuration_possibilities(bits, buttons):
        modified_joltages = list(joltages)
        for i in chain.from_iterable(buttons_pushed):
            if not modified_joltages[i]:
                break

            modified_joltages[i] -= 1
        else:
            new_joltages = tuple(joltage >> 1 for joltage in modified_joltages)
            best = min(best, len(buttons_pushed) + 2*joltage_configuration_cost(new_joltages, buttons))

    return best


with open("input") as f:
    lines = f.readlines()

p1 = 0
p2 = 0
for line in lines:
    diagram, *buttons, joltages = line.split()
    diagram = tuple(map(".#".find, diagram[1:-1]))
    buttons = tuple(tuple(map(int, button[1:-1].split(","))) for button in buttons)
    joltages = tuple(map(int, joltages[1:-1].split(",")))

    p1 += next(map(len, light_configuration_possibilities(diagram, buttons)))
    p2 += joltage_configuration_cost(joltages, buttons)

print(p1, p2)
