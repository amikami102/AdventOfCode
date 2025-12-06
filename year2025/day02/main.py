#year2025/day02/main.py
from pathlib import Path
from textwrap import dedent
from typing import Iterable

from more_itertools import sliced


def parse(txtfile: str) -> Iterable[str]:
    return Path(txtfile).read_text().split(',')


def parse_range(line: str) -> range:
    start, stop = line.split('-')
    return range(int(start), int(stop)+1)


def sequence_repeated_twice(product_id: str) -> bool:
    """Is `product_id` composed of a sequence of digits repeated twice?"""
    midpoint = len(product_id)//2
    first_half, second_half = \
        product_id[:midpoint], product_id[midpoint:]
    return first_half == second_half

def sequence_repeated_twice_or_more(product_id: str) -> bool:
    """
    Is `product_id` composed of a sequence of digits repeated twice or more?
    """
    midpoint = len(product_id)//2
    for k in range(1, midpoint+1):
        uniques = set(sliced(product_id, k))
        if len(uniques) == 1:
            return True
    return False


def solve_part1(data: Iterable[str]) -> int:
    return sum(
        product_id
        for line in data
        for product_id in parse_range(line)
        if sequence_repeated_twice(str(product_id))
    )


def solve_part2(data: Iterable[str]) -> int:
    return sum(
        product_id
        for line in data
        for product_id in parse_range(line)
        if sequence_repeated_twice_or_more(str(product_id))
    )


if __name__ == '__main__':
    print('*************** day 02: gift shop ***************')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""
        Part1: the sum of invalid IDs is {part1}.
        Part 2: the sum of invalid IDs under the new rule in {part2}.
        """))
