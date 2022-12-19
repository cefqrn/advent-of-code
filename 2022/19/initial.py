import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib import parsing

from itertools import product
from functools import cache
from heapq import heappop, heappush
from collections import defaultdict

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))

@cache
def get_possibilities(orc, clc, obco, obcc, gecor, gecob, ore, cla, obs):
    possible_orb = ore // orc
    possible_clb = ore // clc
    possible_obb = min(ore // obco, cla // obcc)
    possible_geb = min(ore // gecor, obs // gecob)
    possibilities: list[tuple[int, int, int, int, int, int, int]] = [(0, 0, 0, 0, 0, 0, 0)] # buy nothing

    for orb, clb, obb, geb in product(range(possible_orb+1), range(possible_clb+1), range(possible_obb+1), range(possible_geb+1)):
        cor = orb * orc + clb * clc + obb * obco + geb * gecor
        ccl = obb * obcc
        cob = geb * gecob

        if cor <= ore and ccl <= cla and cob <= obs:
            possibilities.append((orb, clb, obb, geb, cor, ccl, cob))

    return possibilities


def get_geodes(ore_cost, clay_cost, obs_ore, obs_clay, geode_ore, geode_obs):
    possibilities: list[tuple[int, int, int, int, int, int, int, int, int]] = [(0, 0, 0, 1, 0, 0, 0, 0, 0)]
    best = defaultdict(int)

    possible_geos = []
    while possibilities:
        time, geb, obb, orb, clb, ore, cla, obs, geo = heappop(possibilities)
        
        if geo:print(ore, cla, obs, geo)
        
        ore += orb
        cla += clb
        obs += obb
        geo += geb

        time += 1

        if time == 24:
            if geo:
                possible_geos.append(geo)
            continue

        for dor, dcl, dob, dge, orc1, clc1, obc1 in get_possibilities(ore_cost, clay_cost, obs_ore, obs_clay, geode_ore, geode_obs, ore, cla, obs):
            if geb + dge < best[time]:
                continue

            if geb + dge > best[time]:
                best[time] = geb + dge

            heappush(possibilities, (time, geb+dge, dob+obb, orb+dor, clb+dcl, ore-orc1, cla-clc1, obs-obc1, geo))

    print(possible_geos)

qualities = []
for blueprint in blueprints:
    n, *prices = blueprint
    geodes = get_geodes(*prices)
    qualities.append(n * geodes)
    break


