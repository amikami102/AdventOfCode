from pathlib import Path
import sys
from collections import defaultdict
import re

BALLS_RE = re.compile(r"""
    (
    \d+     # number of balls
    \s
    \b
    \w+     # color of the balls
    \b
    )
    """,
    re.X
)


def parse(filename: str) -> list[list[str]]:
    return [
        BALLS_RE.findall(line)
        for line in Path(filename).read_text().splitlines()
    ]

def split_into_number_and_color(balls: str) -> tuple[int, str]:
    number, color = balls.split()
    return int(number), color


def max_number_per_color(game: list[tuple[str, str]]) -> dict[str, int]:
    grouping = defaultdict(lambda: 0)
    for balls in game:
        number, color = split_into_number_and_color(balls)
        if grouping[color] < number:
             grouping[color] = number
    return grouping 


def is_game_possible(result: dict[str, int], *, red: int, green: int, blue: int) -> bool:
    return red >= result['red'] and blue >= result['blue'] and green >= result['green']


def solve_part1(puzzle_input: list[list[str]]) -> int:
     part1_game = {'red': 12, 'green': 13, 'blue': 14}
     return sum(
         game_id
         for game_id, game in enumerate(puzzle_input, start=1)
         if is_game_possible(max_number_per_color(game), **part1_game) 
     )

def calculate_power(result: dict[str, int]) -> int:
    return result['red'] * result['blue'] * result['green']


def solve_part2(puzzle_input: list[list[str]]) -> int:
    return sum(
        calculate_power(max_number_per_color(game))
        for game in puzzle_input
    )


if __name__ == '__main__':

    title = 'Day 02: Cube Conundrum'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The sum of the id's of possible games is {part1}.
        Part 2: The sum of the powers of these games is {part2}.
        """)
