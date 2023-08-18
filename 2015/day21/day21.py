from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

from itertools import product

base_player_hp = 100

weapons = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0)
]

armors = [
    (0, 0, 0),  # no armor
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5)
]

rings = [
    (0, 0, 0),  # no ring 1
    (0, 0, 0),  # no ring 2
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3)
]

base_boss_hp, boss_damage, boss_armor = map(int, map(lambda x: x.split(': ')[1], s.splitlines()))

def player_wins(player_damage, player_armor):
    player_hp = base_player_hp
    boss_hp = base_boss_hp

    while True:
        boss_hp -= player_damage - boss_armor
        if boss_hp <= 0:
            return True
        
        player_hp -= boss_damage - player_armor
        if player_hp <= 0:
            return False

min_cost = 99999999999
max_cost = -99999999999
for weapon, armor, ring1 in product(weapons, armors, rings):
    for ring2 in rings:
        if ring2 is ring1:
            continue

        cost = weapon[0] + armor[0] + ring1[0] + ring2[0]
        if cost >= min_cost:
            continue

        if player_wins(weapon[1] + ring1[1] + ring2[1], armor[2] + ring1[2] + ring2[2]):
            if cost < min_cost:
                min_cost = cost
        else:
            if cost > max_cost:
                max_cost = cost

print(f"p1: {min_cost}")
print(f"p2: {max_cost}")
