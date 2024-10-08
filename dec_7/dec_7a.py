"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand
consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card
follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any
    other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third
    label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each
    other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly,
77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have
the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid
multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the
strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be
multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is
    stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid
with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""

from collections import namedtuple, Counter
from operator import attrgetter

from common_functions import load_input

FACE_VALUES = {
    "A": "M",
    "K": "L",
    "Q": "K",
    "J": "J",
    "T": "I",
    "9": "H",
    "8": "G",
    "7": "F",
    "6": "E",
    "5": "D",
    "4": "C",
    "3": "B",
    "2": "A",
}

Hand = namedtuple("Hand", "cards bid value alpha")


def get_hand_value(hand: str) -> int:
    unique_vals = list(Counter(hand).values())
    if 5 in unique_vals:
        return 7
    if 4 in unique_vals:
        return 6
    if 3 in unique_vals and 2 in unique_vals:
        return 5
    if 3 in unique_vals and 1 in unique_vals:
        return 4
    if unique_vals.count(2) == 2:
        return 3
    if unique_vals.count(1) == 3:
        return 2
    if unique_vals.count(1) == 5:
        return 1


def get_hand_value_part_2(hand: str) -> int:
    replacement_hand = ""
    most_common = Counter(hand).most_common()
    # Single step to modify list in place and remove Js
    [most_common.remove(c) for c in most_common if c[0] == "J"]
    # This step uses a lambda to order the resulting hand in terms of value from the original dict
    # This could be done more simply by storing the original keys as an ordered string
    # We reverse it since a lower index is required here (e.g. higher value cards should be first)
    sorted(
        most_common, key=lambda x: list(FACE_VALUES.keys()).index(x[0]), reverse=True
    )
    # Whoops! Here's an edge case
    if hand == "JJJJJ":
        print("JJJJ hand!")
        return get_hand_value(hand)
    for letter in hand:
        new_letter = letter
        if letter == "J":
            new_letter = most_common[0][0]
        replacement_hand = replacement_hand + new_letter
    return get_hand_value(replacement_hand)


def transform_hand_to_alpha(hand: str) -> str:
    digits = ""
    for letter in hand:
        digits = digits + FACE_VALUES[letter]
    return digits


if __name__ == "__main__":
    data = load_input("example.txt")
    cards = [
        Hand(
            item.split()[0],
            item.split()[1],
            get_hand_value(item.split()[0]),
            transform_hand_to_alpha(item.split()[0]),
        )
        for item in data
    ]
    print(cards)
    sorted_cards = sorted(cards, key=attrgetter("value", "alpha"))
    print(sorted_cards)
    winnings = 0
    for index, _ in enumerate(sorted_cards):
        winnings += (index + 1) * int(sorted_cards[index].bid)
    print(winnings)
    print("\nPart 2!\n")
    FACE_VALUES = {
        "A": "M",
        "K": "L",
        "Q": "K",
        "T": "J",
        "9": "I",
        "8": "H",
        "7": "G",
        "6": "F",
        "5": "E",
        "4": "D",
        "3": "C",
        "2": "B",
        "J": "A",
    }
    cards = [
        Hand(
            item.split()[0],
            item.split()[1],
            get_hand_value_part_2(item.split()[0]),
            transform_hand_to_alpha(item.split()[0]),
        )
        for item in data
    ]
    print(cards)
    sorted_cards = sorted(cards, key=attrgetter("value", "alpha"))
    print(sorted_cards)
    winnings = 0
    for index, _ in enumerate(sorted_cards):
        winnings += (index + 1) * int(sorted_cards[index].bid)
    print(winnings)
    pass
