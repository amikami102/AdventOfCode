"""
-- Day 01: Sonar Sleep --

Usage example:
    Advent_Of_Code/year2021/day01_sonar_sleep $ python main.py test.txt input.txt
"""
import sys
import pathlib
import itertools
from typing import *


def parse(txt_filename: str) -> list[int]:
    return list(map(int, pathlib.Path(txt_filename).read_text().splitlines()))


def solve_part1(puzzle_input: list[int]) -> int:
    """Count the number of times the ocean depth measurement increased from the previous measurement."""
    return sum(
        m0 < m1
        for m0, m1 in itertools.pairwise(puzzle_input)
    )


def sliding_window(iterable: Iterable, w: int):
    pass


def solve_part2(puzzle_input: list[int]) -> int:
    """
    Count the number of times a sum of sliding window of three measurements increased from the previous sum of sliding window of three measurements.
    """
    pass


if __name__ == '__main__':
    title = 'Day 01: Sonar Sleep'
    print(title.center(50, '+'))

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(data)
        print(f"""{file}
        Part 1: The number of times the ocean depth measurement increased is {part1}.
        Part 2:
        """)
