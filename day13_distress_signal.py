"""
-- Day 13: Distress Signal --

Usage example
    Advent_of_Code/year2022 $ python day13_distress_signal.py day13_test.txt day13_input.txt

Inspired by Peter Norvig for the elegant comparison and sorting
"""
import sys
import json
import pathlib
import math
import functools
import itertools
from typing import *

Packet = list


def parse(txt_filename: str) -> list[tuple[Any, ...]]:
    return [
        tuple(json.loads(packet) for packet in pair.split('\n'))
        for pair in pathlib.Path(txt_filename).read_text().split('\n\n')
    ]


def _compare(left: list | int, right: list | int) -> int:
    """
    Compare the items according to the rules.
    Since the packets are lists, the very first pass through this function is
    actually the list vs list comparison. This is the part that implements the first-nonzero pass rule.
    It is also why this function returns the difference between the integer values instead of a boolean value.
    """
    match isinstance(left, int), isinstance(right, int):
        case True, True:
            return left - right
        case False, True:
            return _compare(left, [right])
        case True, False:
            return _compare([left], right)
        case False, False:
            return next(
                filter(lambda x: x, map(_compare, left, right)),
                False
            ) or len(left) - len(right)


def _right_order(packets: tuple[Packet, Packet]) -> bool:
    """
    Pass the input packets into _compare() and return True if the output of _compare() is negative or zero, which only happens if the packets are identical.
    """
    return _compare(*packets) <= 0


def solve_part1(puzzle_input: list[tuple[Packet, Packet]]) -> int:
    """
    Given a list of pair of packets, sum the indices of pairs
    whose items are in the right order.
    """
    return sum(
        i
        for i, pair in enumerate(puzzle_input, 1)
        if _right_order(pair)
    )


def solve_part2(puzzle_input: list[tuple[Packet]]) -> int:
    """
    Unpair the packets and sort them according to the comparison rule.
    Insert the divider packets ([[2]] and [[6]]) in their appropriate place. Return the product of the indices of the divider packets in the sorted sequence.
    """
    dividers = [[2]], [[6]]
    ordered = sorted(
        list(itertools.chain.from_iterable(puzzle_input)) + list(dividers),
        key=functools.cmp_to_key(_compare)
    )
    return math.prod(ordered.index(d) + 1 for d in dividers)


if __name__ == '__main__':
    title = 'Day 13: Distress Signal'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The sum of the indices of packets that are paired in the right order is {part1}.
        Part 2: The product of the indices of divider packets is {part2}.
        """)
