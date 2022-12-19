import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib import parsing

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))

best = [0]*24
costs = []
def search(time_left, bots, bot_diffs, stores):
    global costs, best

    ore_cost, cla_cost, obs_cost_ore, obs_cost_cla, geo_cost_ore, geo_cost_obs = costs

    ore, cla, obs, geo = stores[0]+bots[0], stores[1]+bots[1], stores[2]+bots[2], stores[3]+bots[3]
    bots = bots[0]+bot_diffs[0], bots[1]+bot_diffs[1], bots[2]+bot_diffs[2], bots[3]+bot_diffs[3]

    time_left -= 1
    if best[time_left] < geo:
        best[time_left] = geo
        print(24 - time_left, bots, geo)
    elif best[time_left] > geo:
        return

    if time_left == 0:
        return

    search(time_left, bots, (0,0,0,0), (ore, cla, obs, geo))  # buying nothing
    if ore >= geo_cost_ore and obs >= geo_cost_obs:
        search(time_left, bots, (0,0,0,1), (ore-geo_cost_ore, cla, obs-geo_cost_obs, geo))
    if ore >= obs_cost_ore and cla >= obs_cost_cla:
        search(time_left, bots, (0,0,1,0), (ore-obs_cost_ore, cla-obs_cost_cla, obs, geo))
    if ore >= cla_cost:
        search(time_left, bots, (0,1,0,0), (ore-cla_cost, cla, obs, geo))
    if ore >= ore_cost:
        search(time_left, bots, (1,0,0,0), (ore-ore_cost, cla, obs, geo))


s = 0
for n, *costs in blueprints:
    best = [0]*24
    search(24, (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
    s += n * best[0]
    print(n, best)

print(s)
