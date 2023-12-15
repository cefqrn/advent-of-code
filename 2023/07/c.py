def rank_hand_1(hand, card_strengths=None):
    if card_strengths is None:
        card_strengths = list(map("23456789TJQKA".index, hand))

    return sorted(map(hand.count,{*hand}))[::-1], card_strengths


def rank_hand_2(hand):
    card_strengths = list(map("J23456789TQKA".index, hand))

    return max(
        rank_hand_1(hand.replace("J", replacement), card_strengths)
        for replacement in set(hand)
    )


*lines, = open(0)
for ranker in rank_hand_1, rank_hand_2:
    ranks = sorted(
        (ranker(hand), int(bid))
        for hand, bid in map(str.split, lines)
    )

    print(sum(
        bid * rank
        for rank, (_, bid) in enumerate(ranks, 1)
    ))
