"""
-- Day 25: Full of Hot Air --

Usage example:
    Advent_Of_Code/year2022 $ python day25_full_of_hot_air.py day25_test.txt day25_input.txt

I learned from Peter Norvig's solution how to convert decimal integers to base-X integers recursively.

Here's a breakdown of how 4857 turns to SNAFU by building a stack.
    4857/5 = 971, 2             => stack = (2)
    971/5 = 194, 1              => stack = (1, 2)
    194/5 = 38, 4   => 39, -1   => stack = (-1, 1, 2)
    39/5 = 7, 4     => 8, -1    => stack = (-1, -1, 1, 2)
    8/5 = 1, 3      => 2, -2    => stack = (-2, -1, -1, 1, 2)
    2/5 = 0, 2                  => stack = (2, -2, -1, -1, 1, 2) and stop because q = 0
SNAFU of 4857 is `''.join(SNAFU_CHAR[r] for r in stack)`.

The main block contains unit tests to test the code on toy examples.
"""
import sys
import pathlib
from typing import *

Snafu = str

SNAFU_DIGITS: dict[Snafu, int] = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}
SNAFU_CHARS: dict[int, Snafu] = {v: k for k, v in SNAFU_DIGITS.items()}


def parse(txt_filename: str) -> list[Sequence[Snafu]]:
    """Return file content as list of Snafu"""
    return pathlib.Path(txt_filename).read_text().splitlines()


def snafu_to_decimal(snafu_seq: Sequence[Snafu]) -> int:
    """
    Convert a sequence of Snafu numbers to a decimal integer,
    which is equivalent to converting base-5 integer to base-10.
    """
    return sum(
        (5 ** idx) * SNAFU_DIGITS[char]
        for idx, char in enumerate(reversed(snafu_seq))
    )


def decimal_to_snafu(decimal: int) -> Sequence[Snafu]:
    """
    Convert decimal integer to Sequence of Snafu digits recursively.

    Let x be a base-10 integer.
        1) x / 5 = (q, r)
        2) If r < 3, do nothing. Otherwise, increment q by 1 and convert r to r - 5
            (so r = 3 becomes -2, r = 4 becomes -1).
        3) Convert q into Snafu recursively except when q = 0, in which case return ''
            and attach SNAFU_DIGITS[r] to the right end.
    """
    q, r = divmod(decimal, 5)
    if r in (3, 4):
        q, r = q + 1, r - 5
    return ''.join((decimal_to_snafu(q) if q else '', SNAFU_CHARS[r]))


def solve_part1(puzzle_input: list[Sequence[Snafu]]) -> Sequence[Snafu]:
    return decimal_to_snafu(sum(map(snafu_to_decimal, puzzle_input)))


if __name__ == '__main__':
    title = 'Day 25: Full of Hot Air'
    print(title.center(50, '-'))

    # test that snafu_to_decimal() works
    assert snafu_to_decimal('0') == 0
    assert snafu_to_decimal('1') == 1
    assert snafu_to_decimal('2') == 2
    assert snafu_to_decimal('1=') == 5 - 2 == 3
    assert snafu_to_decimal('1-') == 5 - 1 == 4
    assert snafu_to_decimal('10') == 5 - 0 == 5
    assert snafu_to_decimal('11') == 5 + 1 == 6
    assert snafu_to_decimal('12') == 5 + 2 == 7
    assert snafu_to_decimal('2=') == 10 - 2 == 8
    assert snafu_to_decimal('2-') == 10 - 1 == 9
    assert snafu_to_decimal('20') == 10
    assert snafu_to_decimal('21') == 10 + 1 == 11
    assert snafu_to_decimal('22') == 10 + 2 == 12
    assert snafu_to_decimal('1==') == 25 - 10 - 2 == 13
    assert snafu_to_decimal('1=-') == 25 - 10 - 1 == 14
    assert snafu_to_decimal('1=0') == 25 - 10 == 15
    assert snafu_to_decimal('1=1') == 25 - 10 + 1 == 16
    assert snafu_to_decimal('1=2') == 25 - 10 + 2 == 17
    assert snafu_to_decimal('1-=') == 25 - 5 - 2 == 18
    assert snafu_to_decimal('1--') == 25 - 5 - 1 == 19
    assert snafu_to_decimal('1-0') == 25 - 5 - 0 == 20

    # test the decimal_to_snafu() works
    assert decimal_to_snafu(21) == '1-1'
    assert decimal_to_snafu(22) == '1-2'
    assert decimal_to_snafu(23) == '10='
    assert decimal_to_snafu(24) == '10-'
    assert decimal_to_snafu(25) == '100'
    assert decimal_to_snafu(106) == '1-11'
    assert decimal_to_snafu(4857) == ''.join(SNAFU_CHARS[r] for r in (2, -2, -1, -1, 1, 2))

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(data)
        print(f"""{file}:
        Part 1: The SNAFU code to supply to Bob is {part1}.
        """)
