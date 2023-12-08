"""
--- Day 1: Trebuchet?! ---

Usage example:
    $ python day01_trebuchet.py day01_test.txt day01_test2.txt day01_input.txt
"""
from typing import Iterator, Callable
from collections import deque
from itertools import islice
from pathlib import Path
import sys

NUMBERS = [
    ('one',     '1'),
    ('two',     '2'),
    ('three',   '3'),
    ('four',    '4'),
    ('five',    '5'),
    ('six',     '6'),
    ('seven',   '7'),
    ('eight',   '8'),
    ('nine',    '9'),
]


def parse(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()


def get_calibration_value(line: str, extract_digits_func: Callable = None) -> int:
    """
    Get the calibration value from `line` by creating a two digit number
    from the first and last numeric characters extracted from `line` 
    by calling `extract_digits_func`.
    """
    digits = list(extract_digits_func(line)) or [0]
    return int(f'{digits[0]}{digits[-1]}')


def solve_part1(puzzle_input: list[str]) -> int:
    """Return the sum of calibration values from each line of `puzzle_input`."""
    return sum(
        get_calibration_value(line, extract_digits)
        for line in puzzle_input
    )

def solve_part2(puzzle_input: list[str]) -> int:
    """Return the sum of real calibration values from each line of `puzzle_input`."""
    return sum(
        get_calibration_value(line, extract_real_digits)
        for line in puzzle_input
    )

def extract_digits(line:str) -> Iterator[int]:
    """Extract digit characters from `line`."""
    return (char for char in line if char.isdigit())


def extract_real_digits(line: str) -> Iterator[int]:
    """Extract digits or words spelling out digits from `line` in the order of appearance."""
    line_it = iter(line)
    window = deque(islice(line_it, 5), maxlen=5)
    for char in line_it:
        substring = ''.join(tuple(window))
        for word, number in NUMBERS:
            if substring.startswith(number) or substring.startswith(word):
                yield number
        window.append(char)

    while window:
        substring = ''.join(tuple(window))
        for word, number in NUMBERS:
            if substring.startswith(number) or substring.startswith(word):
                yield number
        window.popleft()
        

if __name__ == '__main__':

    title = 'Day 1: Trebuchet?!'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The sum of the calibration values is {part1}.
        Part 2: The sum of the real calibartion values is {part2}.
        """)
