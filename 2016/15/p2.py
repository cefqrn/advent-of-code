from itertools import count
from math import lcm
from re import compile

NUM_PATTERN = compile(r"\d+")

# def solve(discs):

with open(0) as f:
    discs_str = f.readlines()

discs = []
for disc in discs_str:
    disc_id, pos_count, time, pos = map(int, NUM_PATTERN.findall(disc))
    discs.append(((pos - disc_id - time) % pos_count, pos_count))

print(discs)

# p1 = solve(discs)
# discs[max(discs) + 1] = 11, 0, 0
# print(p1, solve(discs))
