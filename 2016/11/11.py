from collections import deque
from itertools import combinations
from re import compile

microchip_pattern = compile("(\w+)-compatible microchip")
generator_pattern = compile("(\w+) generator")

def solve(floors_str):
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
      if (floor & microchip_mask) ^ (floor >> generator_offset) & floor and floor >> generator_offset:
        return True
    return False

  def is_done(floors): return not any(floors[:3])

  def get_things_on_floor(floor):
    things = []
    i = 0
    while floor:
      if floor & 1: things.append(i)
      floor >>= 1
      i += 1
    return things

  possibilities = deque([(0, 0, floors)])
  seen = {}
  while possibilities:
    steps, floor, floors = possibilities.popleft()

    if seen.get((floors_tup:=tuple(floors), floor), steps+1) <= steps: continue
    seen[(floors_tup, floor)] = steps

    if is_done(floors): return steps

    def move_if_valid(new_floor, things):
      new_floors = floors.copy()
      new_floors[floor]     &= ~things
      new_floors[new_floor] |=  things
      if is_invalid(new_floors): return
      possibilities.append((steps+1, new_floor, new_floors))

    things = get_things_on_floor(floors[floor])
    for thing_index in things:
      if floor > 0: move_if_valid(floor-1, 1 << thing_index)
      if floor < 3: move_if_valid(floor+1, 1 << thing_index)
    for e1, e2 in combinations(things, 2):
      if floor > 0: move_if_valid(floor-1, 1 << e1 | 1 << e2)
      if floor < 3: move_if_valid(floor+1, 1 << e1 | 1 << e2)

with open(0) as f:
  floors_str = f.readlines()

p1 = solve(floors_str)
floors_str[0] += "An elerium generator An elerium-compatible microchip A dilithium generator A dilithium-compatible microchip"
p2 = solve(floors_str)

print(p1, p2)
