from itertools import count
from re import compile

NUM_PATTERN = compile(r"\d+")

def solve(discs):
    for i in count():
        for disc_id, (pos_count, time, pos) in discs.items():
            if not (i + disc_id + pos - time) % pos_count:
                continue
            break
        else:
            return i

with open(0) as f:
    discs_str = f.readlines()

discs = {}
for disc in discs_str:
    disc_id, pos_count, time, pos = map(int, NUM_PATTERN.findall(disc))
    discs[disc_id] = pos_count, time, pos

p1 = solve(discs)
discs[max(discs) + 1] = 11, 0, 0
print(p1, solve(discs))
