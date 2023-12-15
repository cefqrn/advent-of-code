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


def rank_hand_1(hand, card_strengths=None):
    counts = Counter(hand)
    match max(counts.values()):
        case 5:
            hand_type = 1
        case 4:
            hand_type = 2
        case 3:
            hand_type = 3 if len(counts) == 2 else 4
        case 2:
            hand_type = 5 if len(counts) == 3 else 6
        case 1:
            hand_type = 7

    if card_strengths is None:
        card_strengths = list(map("AKQJT98765432".index, hand))

    return hand_type, card_strengths


def rank_hand_2(hand: str):
    card_strengths = list(map("AKQT98765432J".index, hand))

    return min(
        rank_hand_1(hand.replace("J", replacement), card_strengths)
        for replacement in set(hand)
    )


for ranker in rank_hand_1, rank_hand_2:
    ranks = sorted(
        (ranker(hand), int(bid))
        for hand, bid in map(str.split, lines)
    )

    print(sum(
        bid * rank
        for rank, (_, bid) in enumerate(reversed(ranks), 1)
    ))
