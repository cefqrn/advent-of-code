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

from dataclasses import dataclass
from itertools import combinations_with_replacement
from re import findall


@dataclass
class Ingredient:
    capacity:   int
    durability: int
    flavor:     int
    texture:    int
    calories:   int

    @property
    def score(self):
        return max(self.capacity, 0) * max(self.durability, 0) * max(self.flavor, 0) * max(self.texture, 0)

    def __add__(self, other: Ingredient):
        return Ingredient(
            self.capacity   + other.capacity,
            self.durability + other.durability,
            self.flavor     + other.flavor,
            self.texture    + other.texture,
            self.calories   + other.calories
        )
    
    def __gt__(self, other: Ingredient):
        return self.score > other.score


ingredients = [
    Ingredient(*map(int, findall(r"-?\d+", l))) for l in s.splitlines()
]

BASE = Ingredient(0, 0, 0, 0, 0)

best_p1 = None
best_p2 = None
best_p1_score = 0
best_p2_score = 0
for recipe in map(lambda r: sum(r, BASE), combinations_with_replacement(ingredients, r=100)):
    score = recipe.score

    if score > best_p1_score:
        best_p1 = recipe
        best_p1_score = score

    if recipe.calories == 500 and score > best_p2_score:
        best_p2 = recipe
        best_p2_score = score

print(f"p1: {best_p1_score}")
print(f"p2: {best_p2_score}")
