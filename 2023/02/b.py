from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    games = f.read().rstrip().splitlines()

from operator import le
from math import prod
from re import findall


def least_required_of(color: str, game: str) -> int:
    return max(map(int, findall(fr"\d+(?= {color})", game)), default=0)


colors = {"red": 12, "green": 13, "blue": 14}

p1 = p2 = 0
for game in games:
    game_id, _ = game.split(": ", 1)

    least_required = [
        least_required_of(color, game)
        for color in colors
    ]

    p2 += prod(least_required)
    if all(map(le, least_required, colors.values())):
        p1 += int(game_id.split()[1])

print(p1, p2)
