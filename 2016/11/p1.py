from collections import deque
from itertools import combinations
from re import compile

microchip_pattern = compile("(\w+)-compatible microchip")
generator_pattern = compile("(\w+) generator")

with open(0) as f:
    floors_str = f.readlines()

floors_str[0] += "An elerium generator An elerium-compatible microchip A dilithium generator A dilithium-compatible microchip"

floors = [0] * 4
elements = microchip_pattern.findall(" ".join(floors_str))
generator_offset = len(elements)

for i, floor_str in enumerate(floors_str):
    for microchip in microchip_pattern.findall(floor_str):
        floors[i] |= 1 << elements.index(microchip)
    
    for generator in generator_pattern.findall(floor_str):
        floors[i] |= 1 << (elements.index(generator) + generator_offset)

microchip_mask = 2**generator_offset - 1
def is_invalid(floors):
    for floor in floors:
        # if there are microchips that don't have generators and there are generators
        if (floor & microchip_mask) ^ (floor >> generator_offset) & floor and floor >> generator_offset:
            return True
    return False

def is_done(floors):
    return not any(floors[:3])

def get_things_on_floor(floor):
    things = []
    i = 0
    while floor:
        if floor & 1:
            things.append(i)
        floor >>= 1
        i += 1
    return things

possibilities: deque[int, int, list[int]] = deque([(0, 0, floors)])
seen = {}
prev_steps = 0
while possibilities:
    step_count, current_floor, floors = possibilities.popleft()
    if step_count > prev_steps:
        prev_steps = step_count
        print(f"checking {step_count}")

    if seen.get((floors_tup:=tuple(floors), current_floor), step_count+1) <= step_count:
        continue

    seen[(floors_tup, current_floor)] = step_count

    if is_done(floors):
        print(step_count)
        break

    def move_if_valid(new_floor, things):
        new_floors = floors.copy()
        new_floors[current_floor] &= ~things
        new_floors[new_floor    ] |=  things
        if is_invalid(new_floors): return

        possibilities.append((step_count+1, new_floor, new_floors))

    things = get_things_on_floor(floors[current_floor])
    for thing_index in things:
        if current_floor > 0:
            move_if_valid(current_floor-1, 1 << thing_index)
        if current_floor < 3:
            move_if_valid(current_floor+1, 1 << thing_index)
    
    for e1, e2 in combinations(things, 2):
        if current_floor > 0:
            move_if_valid(current_floor-1, 1 << e1 | 1 << e2)
        if current_floor < 3:
            move_if_valid(current_floor+1, 1 << e1 | 1 << e2)
