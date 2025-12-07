# year2025/day03/main.py
from pathlib import Path
from textwrap import dedent
from typing import Iterable, Iterator

from more_itertools import spy


def parse(txtfile: str) -> Iterable[str]:
    return Path(txtfile).read_text().splitlines()

def parse_bank(line: str) -> list[int]:
    return [int(s) for s in list(line)]

# def select_largest_joltage(batteries: list[int]) -> int:
#     tens_digit = max(batteries[:-1])
#     ones_digit = max(batteries[batteries.index(tens_digit)+1:])
#     return tens_digit * 10 + ones_digit

def select_largest_joltage(batteries: list[int], n: int):
    need = n
    while need > 0:
        digit = max(batteries[: - need + 1]) if need > 1 else max(batteries)
        yield digit * (10 ** (need -1))
        batteries = batteries[batteries.index(digit) + 1:]
        need -= 1
        if len(batteries) == need:
            for digit, k in zip(batteries, range(need, 0, -1)):
                yield digit * (10 ** (k-1))
            need = 0

def solve_part1(data: Iterable[str]) -> int:
    return sum(
        sum(select_largest_joltage(parse_bank(bank), 2))
        for bank in data
    )

def solve_part2(data: Iterable[str]) -> int:
    return sum(
        sum(select_largest_joltage(parse_bank(bank), 12)) 
        for bank in data)

if __name__ == '__main__':
    print('-------- day 03: lobby --------')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""\
        part1: the total output joltage is {part1}.
        part2: the new total output joltage is {part2}."""))

