import sys
from typing import *
from pathlib import Path
import re
from itertools import pairwise


def extract_integers(text: str) -> tuple[int, ...]:
    """Capture negative or positive integers in `text`."""
    return tuple(int(num) for num in re.findall(r'-?\d+', text))


def parse(txtfile) -> list[tuple[int]]:
    return [
        extract_integers(line) 
        for line in Path(txtfile).read_text().splitlines()
    ]


def take_successive_differences(sequence: Sequence[int]) -> Sequence[int]:
    """Take successive differences of `sequence`."""
    return [second - first for first, second in pairwise(sequence)]


def extrapolate(sequence: Sequence[int], *, previous: bool = False) -> int:
    """
    Recursively extrapolate the next value of `sequence` using difference tables.
    If previous is True, extrapolate the value before the beginning of the sequence.
    """
    if all(term == 0 for term in sequence):
        return 0
    else:
        last_term, sign = (sequence[-1], 1) if not previous else (sequence[0], -1)
        last_extrapolation = extrapolate(
            take_successive_differences(sequence), 
            previous=previous
        )
        return last_term + last_extrapolation * sign


def solve_part1(puzzle_input) -> int:
    return sum(
        extrapolate(history)
        for history in puzzle_input
    )


def solve_part2(puzzle_input):
    return sum(
        extrapolate(history, previous=True)
        for history in puzzle_input
    )


if __name__ == '__main__':

    title = 'Day 09: Mirage maintenance'
    print(title.center(50, '-'))

    for filename in sys.argv[1:]:
        data = parse(filename)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{filename}
        Part 1: The sum of the extrapolated values is {part1}.
        Part 2: The sum of the exprapolated values is {part2}.
        """)
