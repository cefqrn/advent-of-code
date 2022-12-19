import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib import *
from math import ceil

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))

TOTAL_TIME = 32


def search(time_left, bots, bot_diffs, stores):
    global costs, best

    ore_cost, cla_cost, obs_cost_ore, obs_cost_cla, geo_cost_ore, geo_cost_obs = costs

    ore, cla, obs, geo = stores[0]+bots[0], stores[1]+bots[1], stores[2]+bots[2], stores[3]+bots[3]
    bots = bots[0]+bot_diffs[0], bots[1]+bot_diffs[1], bots[2]+bot_diffs[2], bots[3]+bot_diffs[3]

    time_left -= 1
    if time_left < 0:
        return

    if best[time_left] < geo:
        best[time_left] = geo
        print(TOTAL_TIME - time_left, bots, geo)
    elif best[time_left] > geo:
        return

    # ore
    if ore >= ore_cost:
        search(time_left, bots, (1,0,0,0), (ore-ore_cost, cla, obs, geo))
    else:  # wait for ore
        t = ceil((ore_cost-ore)/bots[0])  # wait time
        search(time_left-t, bots, (1,0,0,0), (ore+bots[0]*t-ore_cost, cla+bots[1]*t, obs+bots[2]*t, geo+bots[3]*t))

    # cla
    if ore >= cla_cost:
        search(time_left, bots, (0,1,0,0), (ore-cla_cost, cla, obs, geo))
    else:
        t = ceil((cla_cost-ore)/bots[0])
        search(time_left-t, bots, (0,1,0,0), (ore+bots[0]*t-cla_cost, cla+bots[1]*t, obs+bots[2]*t, geo+bots[3]*t))

    # obs
    if ore >= obs_cost_ore and cla >= obs_cost_cla:
        search(time_left, bots, (0,0,1,0), (ore-obs_cost_ore, cla-obs_cost_cla, obs, geo))
    elif bots[1]:
        t = max(ceil((obs_cost_ore-ore)/bots[0]), ceil((obs_cost_cla-cla)/bots[1]))
        search(time_left-t, bots, (0,0,1,0), (ore+bots[0]*t-obs_cost_ore, cla+bots[1]*t-obs_cost_cla, obs+bots[2]*t, geo+bots[3]*t))

    # geo
    if ore >= geo_cost_ore and obs >= geo_cost_obs:
        search(time_left, bots, (0,0,0,1), (ore-geo_cost_ore, cla, obs-geo_cost_obs, geo))
    elif bots[2]:
        t = max(ceil((geo_cost_ore-ore)/bots[0]), ceil((geo_cost_obs-obs)/bots[2]))
        search(time_left-t, bots, (0,0,0,1), (ore+bots[0]*t-geo_cost_ore, cla+bots[1]*t, obs+bots[2]*t-geo_cost_obs, geo+bots[3]*t))

s = 1
for n, *costs in blueprints[:3]:
    best = [0]*TOTAL_TIME
    search(TOTAL_TIME, (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
    s *= best[0]
    print(n, best)

print(s)
