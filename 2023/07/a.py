from contextlib import suppress
from itertools import groupby
from pathlib import Path

with (Path(__file__).parent / "input").open() as f:
    data = f.read().rstrip()

lines = data.splitlines()
blocks = [tuple(group) for has_content, group in groupby(lines, bool) if has_content]
with suppress(ValueError):
    ints = [int(x) for x in data.split()]

from collections import Counter
from bisect import insort


def rank_hand(hand, values=None):
    if values is None:
        values = list(map("AKQJT98765432".index, hand))

    cards = Counter(hand)
    for count in sorted(cards.values(), reverse=True):
        if count == 5:
            return [1, values]
        if count == 4:
            return [2, values]
        if count == 3:
            if 2 in cards.values():
                return [3, values]

            return [4, values]
        if count == 2:
            if list(cards.values()).count(2) == 2:
                return [5, values]

            return [6, values]

        return [7, values]


def rank_hand_j(hand: str):
    cards_set = set(hand)
    values = list(map("AKQT98765432J".index, hand))

    return min(
        rank_hand(hand.replace("J", replacement), values)
        for replacement in cards_set
    )


for ranker in rank_hand, rank_hand_j:
    ranks = []
    for hand, bid in map(str.split, lines):
        insort(ranks, (ranker(hand), int(bid)))

    winnings = 0
    for rank, (_, bid) in enumerate(reversed(ranks), 1):
        winnings += bid*rank

    print(winnings)
