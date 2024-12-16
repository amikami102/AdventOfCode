import sys
from pathlib import Path
from collections import namedtuple, Counter
from operator import attrgetter


Bid = namedtuple('Bid', ['hand', 'strength', 'bid'])

CARDS = '**23456789TJQKA'
CARDS_WITH_JOKER = '*J23456789T*QKA'


def parse(filename: str) -> list[tuple[str, str]]:
    return [
        tuple(line.split(' '))
        for line in Path(filename).read_text().splitlines()
    ]


def get_hand_type(hand: str, joker_included: bool = False) -> list[int]:
    """
    Based on Peter Norvig's insight that camel card hands can be ranked 
    the same way you would sort the seven partitions of 5.
    Namely, the hands ranked from highest to lowest are:
        Five of a kind  (e.g. 'AAAAA') -> [5]           
        Four of a kind  (e.g. 'AAAA4') -> [4, 1]        
        Full house      (e.g. 'AAA33') -> [3, 2]        
        Three of a kind (e.g. 'AAA43') -> [3, 1, 1]     
        Two pair        (e.g. 'AA335') -> [2, 2, 1]    
        One pair        (e.g. 'AA345') -> [2, 1, 1, 1]  
        High card       (e.g. 'A2386'] -> [1, 1, 1, 1, 1]
    """
    if not joker_included:
        return sorted(Counter(hand).values(), reverse=True)
    else: 
        n_joker = hand.count('J')
        hand_without_joker = Counter(card for card in hand if card != 'J')
        most_common_card, _ = \
            hand_without_joker.most_common(1)[0] if n_joker < 5 else ('J', None)
        hand_without_joker.update(
            {most_common_card: n_joker}
        )
        return sorted(Counter(hand_without_joker).values(), reverse=True)


def get_strength(hand: str, *, joker_included: bool = False) -> list[int]:
    ordering = CARDS if not joker_included else CARDS_WITH_JOKER
    return [ordering.index(card) for card in hand]


def rank_and_add_up_bids(bids: list[Bid]) -> int:
    hands_sorted = sorted(bids, key=attrgetter('hand', 'strength'))
    return sum(
        rank * bid
        for rank, (_, _, bid) in enumerate(hands_sorted, start=1)
    )


def solve_part1(puzzle_input: list[tuple[str, str]]) -> int:
    bids = [
        Bid(get_hand_type(hand), get_strength(hand), int(bid))
        for hand, bid in puzzle_input
    ]
    return rank_and_add_up_bids(bids)
        
    
def solve_part2(puzzle_input: list[tuple[str, str]]) -> int:
    bids = [
        Bid(
            get_hand_type(hand, joker_included = True), 
            get_strength(hand, joker_included=True), 
            int(bid)
        )
        for hand, bid in puzzle_input
    ]
    return rank_and_add_up_bids(bids)


if __name__ == '__main__':
    title = 'Day 07: Camel cards'
    print(title.center(50, '-'))

    assert get_hand_type('QJJQ2', True) == [4, 1]
    assert get_strength('QJJQ2', True) == [12, 1, 1, 12, 2]

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The total winning is {part1}.
        Part 2: The number of ways to win this long race is {part2}.
        """)
