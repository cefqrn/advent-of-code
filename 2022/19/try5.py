import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib import parsing

from bisect import insort

from enum import Enum, auto

class Bot(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()

blueprints = []
for line in lines:
    blueprints.append(parsing.get_ints(line))

best = [0]*24
def bot_is_possible(time_left, costs, bots, bot, stores):
    ore_cost, cla_cost, obs_cost_ore, obs_cost_cla, geo_cost_ore, geo_cost_obs = costs
    geo, obs, cla, ore = stores

    time_left -= 1

    if time_left == 0:
        return False

    if bot is Bot.ORE:
        return ore >= ore_cost
    elif bot is Bot.CLAY:
        if ore >= cla_cost:
            return True
        
        # return bot_is_possible(time_left + bots[])
        

        # insort(possibilities, (bots, time_left, bots, (0,0,1,0), (geo, obs, cla, ore-cla_cost)))
    elif bot is Bot.OBSIDIAN:
        if ore >= obs_cost_ore and cla >= obs_cost_cla:
            return True
        

        # insort(possibilities, (bots, time_left, bots, (0,1,0,0), (geo, obs, cla-obs_cost_cla, ore-obs_cost_ore)))
    else:  # bot is Bot.GEODE:
        if ore >= geo_cost_ore and obs >= geo_cost_obs:
            return True

        
        # insort(possibilities, (bots, time_left, bots, (1,0,0,0), (geo, obs-geo_cost_obs, cla, ore-geo_cost_ore)))

    return False


s = 0
for n, *costs in blueprints:
    best = [0]*24

    nearest = bot_is_possible(24, costs, (0, 0, 0, 1), (0, 0, 0, 0), (0, 0, 0, 0))
    # while nearest is not None:
        # nearest = bot_is_possible(nearest[0], costs, nearest[1], nearest[2], nearest[3])

    s += n * best[0]
    print(n, best)
    break

print(s)
