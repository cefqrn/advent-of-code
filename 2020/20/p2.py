import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

tiles = {}
for block in blocks:
    tile_id, *tile = block.splitlines()
    tile_id = int(tile_id[5:-1])
    tiles[tile_id] = tile

from aoclib.grid import *

def flip(g):
    return [l[::-1] for l in g]

def rotate(g, r=1):
    for _ in range(r % 4):  # clockwise
        g = flip(transpose(g))

    return g


from enum import IntEnum


class Rotation(IntEnum):
    # amount of rotations to get the side at the top
    North = 0
    South = 2
    East = 3
    West = 1

    @property
    def complement(self):
        return Rotation((self.value + 2) % 4)
    

rotations = [Rotation.North, Rotation.South, Rotation.East, Rotation.West]

from collections import defaultdict
sides = defaultdict(lambda: [0, 0, 0, 0])
modified_tiles = {}

start_tile_id, start_tile = tiles.popitem()
unchecked = [(direction, (start_tile_id, start_tile)) for direction in rotations]

modified_tiles[start_tile_id] = start_tile

from itertools import chain
while unchecked:
    rotation, (start_id, start) = unchecked.pop()
    # print("finding", start_id, rotation.name)
    if sides[start_id][rotation]:
        # print("already found")
        continue

    start = rotate(start, rotation)

    for tile_id, tile in tiles.items():
        if tile_id == start_id:
            continue

        flipped = flip(tile)
        for modified_tile in chain((rotate(tile, r) for r in rotations), (rotate(flipped, r) for r in rotations)):
            if flip(start)[0] == rotate(modified_tile, rotation.complement)[0]:
                # print("found", tile_id, start[0])
                # print_grid(rotate(start, rotation.complement))
                # print()
                # print_grid(modified_tile)
                modified_tiles[tile_id] = modified_tile
                unchecked.extend((new_rotation, (tile_id, modified_tile)) for new_rotation in rotations)
                sides[start_id][rotation] = tile_id
                sides[tile_id][rotation.complement] = start_id
                break
        else:
            continue
        break

# print(sides)
# for tile_id, side in sides.items():
#     print(tile_id, sum(map(bool, side)))

# from math import prod
# print(prod(tile_id for tile_id, side in sides.items() if sum(map(bool, side)) == 2))

top_left_id = None
for tile_id, side in sides.items():
    if side[Rotation.East] and side[Rotation.South] and not (side[Rotation.North] or side[Rotation.West]):
        top_left_id = tile_id
        break

if top_left_id is None:
    raise ValueError("Top left not found")

left = top_left_id

horiz = []
while left:
    new = left
    block = [l[1:-1] for l in modified_tiles[new]]
    while new:
        if new != left:
            block = list(map(lambda a, b: a + b[1:-1], block, modified_tiles[new]))

        new = sides[new][Rotation.East]
    
    horiz.extend(block[1:-1])
    left = sides[left][Rotation.South]


from re import compile
p1 = compile(r".(?=.................#.)")
p2 = compile(r"#(?=....##....##....###)")
p3 = compile(r".(?=#..#..#..#..#..#...)")

c = 0
flipped_horiz = flip(horiz)
for g in chain((rotate(horiz, r) for r in rotations), (rotate(flipped_horiz, r) for r in rotations)):
    for l1, l2, l3 in zip(g, g[1:], g[2:]):
        for m in p1.finditer(l1):
            if p2.match(l2[m.start():m.start()+20]) and p3.match(l3[m.start():m.start()+20]):
                c += 1
    if c:
        c *= -15
        for l in g:
            c += l.count('#')
        break

print(c)