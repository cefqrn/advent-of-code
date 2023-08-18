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


from collections import defaultdict
counts = defaultdict(int)

from itertools import combinations
for (id_1, tile_1), (id_2, tile_2) in combinations(tiles.items(), r=2):
    tile_1s = [rotate(tile_1, r) for r in range(4)]
    flipped = flip(tile_2)
    for i in range(4):
        for tile in tile_1s:

            if tile[0] == rotate(tile_2, i)[0] or tile[0] == rotate(flipped, i)[0]:
                print(id_1, id_2)
                counts[id_1] += 1
                counts[id_2] += 1
                break

print(counts)
from math import prod
print(prod(tile_id for tile_id, match_count in counts.items() if match_count == 2))
