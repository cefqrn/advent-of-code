from collections import deque, defaultdict
from bisect import insort

with open(0) as f:
    instructions = f.readlines()

p1 = 0

bots = defaultdict(list)
outputs = defaultdict(list)
for instruction in instructions:
    if instruction.startswith("value"):
        _, value, *_, target_id = instruction.split()
        value, target_id = int(value), int(target_id)

        insort(bots[target_id], value)
        continue

    _, bot_id, *_, lo_target, lo_target_id, _, _, _, hi_target, hi_target_id = instruction.split()
    bot_id, lo_target_id, hi_target_id = int(bot_id), int(lo_target_id), int(hi_target_id)

    if 17 in bots[bot_id] and 61 in bots[bot_id]:
        p1 = bot_id

    try:
        lo, hi = bots[bot_id]
    except ValueError:
        instructions.append(instruction)
        continue

    if lo_target == "output":
        outputs[lo_target_id].append(lo)
    else:
        insort(bots[lo_target_id], lo)
    
    if hi_target == "output":
        outputs[hi_target_id].append(hi)
    else:
        insort(bots[hi_target_id], hi)        

from math import prod
print(p1, prod(outputs[i][-1] for i in range(3)))
