"""
-- Day 4 camp cleanup --

Usage example
    Advent_Of_Code/year2022 $ python day04_camp_cleanup.py day04_test.txt day04_input.txt
"""
import sys
import pathlib
import itertools
from typing import *


def parse(txt_filename: str) -> Iterable[tuple[int, ...]]:
    """
    Each line of the file is '{left1}-{right1},{left2}-{right2}'.
    Parse each line as a tuple of four integers.
    """
    pairs = []
    for line in pathlib.Path(txt_filename).read_text().splitlines():
        pairs.append(
            tuple(
                map(int,
                    itertools.chain.from_iterable(
                        map(
                            lambda pair: tuple(pair.split('-')),
                            line.strip('\n').split(',')
                        )
                    )
                )
            )
        )
    return pairs


def expand_assignments(*pair) -> tuple[set[int], set[int]]:
    """
    For each pair of elves, get the range of sections each elf covers and return
    each range as a set of integers in those ranges.
    """
    left1, right1, left2, right2 = pair
    return set(range(left1, right1 + 1)), set(range(left2, right2 + 1))


def solve_part1(pairs: Iterable[tuple[int,...]]):
    """Count how many pairs have one elf's sections properly contain the other elf's sections"""
    counter: int = 0
    for pair in pairs:
        first, second = expand_assignments(*pair)
        counter += 1 if first.issubset(second) or second.issubset(first) else 0
    return counter


def solve_part2(pairs: Iterable[tuple[int, ...]]):
    """Count how many pairs have any overlap at all"""
    counter: int = 0
    for pair in pairs:
        first, second = expand_assignments(*pair)
        counter += 1 if first.intersection(second) != set() else 0
    return counter


if __name__ == '__main__':
    title = 'Day 04: Camp Cleanup'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)

        print(f"""{path}:
        Part 1: The number of pairs where one elf's assignment fully contains the other's is {part1}.
        Part 2: The number of pairs where the assignments overlap is {part2}.
        """)
