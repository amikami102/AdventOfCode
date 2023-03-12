"""
-- Day 03: Rucksack Reorganization --

Usage example
    Advent_Of_Code_2022 $ python day03_rucksack_reorganization.py day03_test.py day03_input.txt
"""
import sys
import string
import itertools
import pathlib
from typing import *

T = TypeVar('T')

PRIORITY_LEVEL: dict[str, int] = {
    letter: val + 1
    for val, letter in enumerate([*string.ascii_lowercase, *string.ascii_uppercase])
}


def parse(txt_filename: str) -> list[str]:
    """
    Return a list of strings.
    e.g. ['abAB', 'cdCO', ...]
    """
    return pathlib.Path(txt_filename).read_text().splitlines()


def solve_part1(rucksacks: list[str]) -> int:
    """
    Split each rucksack in equal-length compartments.
    Find the item (str) that appear in both compartments.
    Return the sum of the integers representing the overlapping items of each rucksack's compartments.
    """
    out: int = 0
    for rucksack in rucksacks:
        first, second = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
        item = set(first).intersection(set(second)).pop()
        out += PRIORITY_LEVEL[item]
    return out


def solve_part2(rucksacks: list[str]) -> int:
    """
    Group rucksacks into groups of three and find the item common to all three in the group.
    Return the sum of the priority levels of the groups' common items.
    """

    def grouper(iterable: Iterable[T], n: int, fillvalue: T = None) -> Iterator:
        """
        Group an iterable into groups of size n.
        e.g. 'ABCDEFG' will be grouped into 'AB','CD','EF', 'G' if fillvalue is None.
        """
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    out: int = 0
    for group in grouper(rucksacks, n=3):
        first, second, third = group
        badge = set(first).intersection(set(second)).intersection(set(third)).pop()
        out += PRIORITY_LEVEL[badge]
    return out


if __name__ == '__main__':
    title = 'Day 03: Rucksack Reorganization'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The sum of the priority levels is {part1}.
        Part 2: The sum of the priority levels of the badge items is {part2}.
        """)
