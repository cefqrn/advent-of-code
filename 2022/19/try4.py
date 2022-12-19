import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib import parsing

from bisect import insort

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))

best = [0]*24
def search(time_left, costs, bots, bot_diffs, stores):
    possibilities = [(bots, time_left, bots, bot_diffs, stores)]
    while possibilities:
        _, time_left, bots, bot_diffs, stores = possibilities.pop()

        if bots[0]:
            return [time_left, bots, bot_diffs, stores]

        ore_cost, cla_cost, obs_cost_ore, obs_cost_cla, geo_cost_ore, geo_cost_obs = costs

        geo, obs, cla, ore = stores[0]+bots[0], stores[1]+bots[1], stores[2]+bots[2], stores[3]+bots[3]
        bots = bots[0]+bot_diffs[0], bots[1]+bot_diffs[1], bots[2]+bot_diffs[2], bots[3]+bot_diffs[3]

        time_left -= 1
        if best[time_left] < geo:
            best[time_left] = geo
            print(24 - time_left, bots, geo)
        elif best[time_left] > geo:
            continue

        if time_left == 0:
            continue

        insort(possibilities, (bots, time_left, bots, (0,0,0,0), (geo, obs, cla, ore)))  # buying nothing
        if ore >= geo_cost_ore and obs >= geo_cost_obs:
            insort(possibilities, (bots, time_left, bots, (1,0,0,0), (geo, obs-geo_cost_obs, cla, ore-geo_cost_ore)))
        if ore >= obs_cost_ore and cla >= obs_cost_cla:
            insort(possibilities, (bots, time_left, bots, (0,1,0,0), (geo, obs, cla-obs_cost_cla, ore-obs_cost_ore)))
        if ore >= cla_cost:
            insort(possibilities, (bots, time_left, bots, (0,0,1,0), (geo, obs, cla, ore-cla_cost)))
        if ore >= ore_cost:
            insort(possibilities, (bots, time_left, bots, (0,0,0,1), (geo, obs, cla, ore-ore_cost)))

    return None


s = 0
for n, *costs in blueprints:
    best = [0]*24

    nearest = search(24, costs, (0, 0, 0, 1), (0, 0, 0, 0), (0, 0, 0, 0))
    while nearest is not None:
        nearest = search(nearest[0], costs, nearest[1], nearest[2], nearest[3])

    s += n * best[0]
    print(n, best)
    break

print(s)
