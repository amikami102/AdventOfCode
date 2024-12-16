import sys
from pathlib import Path
import re


def parse(filename: str) -> list[tuple[list, list]]:
    return [
        parse_line(card_line)
        for card_line in Path(filename).read_text().splitlines()
    ]

def parse_line(card_line: str) -> tuple[list[str], list[str]]:
    before, _,  after = re.sub(r'Card\s+\d+:', '', card_line).partition('|')
    return re.findall(r'\d+', before), re.findall(r'\d+', after)


def count_matches(winners: list[str], numbers_drawn: list[str]) -> int:
    return len(
        set(winners).intersection(set(numbers_drawn))
    )


def calculate_points(n_matches: int) -> int:
    return 2 ** (n_matches - 1) if n_matches else 0


def solve_part1(puzzle_input) -> int:
    return sum(
        calculate_points(count_matches(*card))
        for card in puzzle_input
    )
        

def solve_part2(puzzle_input) -> int:
    n_cards = len(puzzle_input)
    matches = {
        card_num: count_matches(*card)
        for card_num, card in enumerate(puzzle_input, start=1)
    }
    cards = [k + 1 for k in range(n_cards)]
    counter = 0
    while cards:
        current = cards.pop()
        counter += 1
        if current <= n_cards:
            cards.extend(
                [
                    current + (k + 1)
                    for k in range(matches[current])
                    if current + k + 1 <= n_cards
                ]
            )
    return counter




if __name__ == '__main__':

    title = 'Day 04: Scratchcards'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The sum of the points is {part1}.
        Part 2: The total number of scratchcards is {part2}.
        """)
