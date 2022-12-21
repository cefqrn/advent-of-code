import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib import parsing

from math import ceil

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))


def search(time_left, bots, new_bot, stores):
    global costs, best, state_count

    ore_cost, cla_cost, obs_cost_ore, obs_cost_cla, geo_cost_ore, geo_cost_obs = costs
    possible = [(time_left, bots, new_bot, stores)]

    while possible:
        time_left, bots, new_bot, stores = possible.pop()

        state_count += 1

        time_left -= 1
        if time_left < 0:
            continue

        ore, cla, obs, geo = stores[0]+bots[0], stores[1]+bots[1], stores[2]+bots[2], stores[3]+bots[3]
        bots[new_bot] += 1

        if best[time_left] > geo:
            continue
        
        best[time_left] = geo

        # ore
        if ore >= ore_cost:
            possible.append((time_left, bots.copy(), 0, (ore-ore_cost, cla, obs, geo)))
        else:  # wait for ore
            t = ceil((ore_cost-ore)/bots[0])  # wait time
            if time_left - t >= 0:
                possible.append((time_left-t, bots.copy(), 0, (ore+bots[0]*t-ore_cost, cla+bots[1]*t, obs+bots[2]*t, geo+bots[3]*t)))

        # cla
        if ore >= cla_cost:
            possible.append((time_left, bots.copy(), 1, (ore-cla_cost, cla, obs, geo)))
        else:
            t = ceil((cla_cost-ore)/bots[0])
            if time_left - t >= 0:
                possible.append((time_left-t, bots.copy(), 1, (ore+bots[0]*t-cla_cost, cla+bots[1]*t, obs+bots[2]*t, geo+bots[3]*t)))

        # obs
        if ore >= obs_cost_ore and cla >= obs_cost_cla:
            possible.append((time_left, bots.copy(), 2, (ore-obs_cost_ore, cla-obs_cost_cla, obs, geo)))
        elif bots[1]:
            t = max(ceil((obs_cost_ore-ore)/bots[0]), ceil((obs_cost_cla-cla)/bots[1]))
            if time_left - t >= 0:
                possible.append((time_left-t, bots.copy(), 2, (ore+bots[0]*t-obs_cost_ore, cla+bots[1]*t-obs_cost_cla, obs+bots[2]*t, geo+bots[3]*t)))

        # geo
        if ore >= geo_cost_ore and obs >= geo_cost_obs:
            possible.append((time_left, bots.copy(), 3, (ore-geo_cost_ore, cla, obs-geo_cost_obs, geo)))
        elif bots[2]:
            t = max(ceil((geo_cost_ore-ore)/bots[0]), ceil((geo_cost_obs-obs)/bots[2]))
            if time_left - t >= 0:
                possible.append((time_left-t, bots.copy(), 3, (ore+bots[0]*t-geo_cost_ore, cla+bots[1]*t, obs+bots[2]*t-geo_cost_obs, geo+bots[3]*t)))

from time import perf_counter
s = 0
for n, *costs in blueprints:
    st = perf_counter()
    best = [0]*24
    state_count = 1
    search(24, [0, 0, 0, 0], 0, (1, 0, 0, 0))
    print(n, state_count, f"in {perf_counter() - st:.02f}s")
    s += n * best[0]
    print(best)

print(s)
