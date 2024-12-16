from typing import *
import sys
from pathlib import Path
import string
import re
import functools
from operator import mul


Coordinate = tuple[int, int]

SYMBOLS = {
    symbol for symbol in string.punctuation
    if symbol != '.'
}
GEAR = '*'
DIRECTIONS = [
    (1, 0), (-1, 0), (0, -1), (0, 1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]


def parse(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()


def locate_symbols(grid: list[str], symbols: set[str] = SYMBOLS) -> list[Coordinate]:
    return [
        (i, j)
        for i, row in enumerate(grid)
        for j, character in enumerate(row)
        if character in symbols
    ]


def find_parts(grid: list[str]) -> dict[Coordinate, re.Match]:
    return {
        (i, j): match
        for i, row in enumerate(grid)
        for match in re.finditer(r'\d+', row)
        for j in range(match.start(), match.end())
    }


def yield_part_if_adjacent(
        parts: dict[Coordinate, int], 
        symbol_locations: list[Coordinate]
    ) -> set[re.Match]:
    return {
        parts[(row + drow, col + dcol)]
        for row, col in symbol_locations
        for (drow, dcol) in DIRECTIONS
        if parts.get((row + drow, col + dcol), None)
    }


def yield_gear_ratio(parts: dict[Coordinate, int], gear_locations: list[Coordinate]):
    for row, col in gear_locations:
        adjacent_parts = {
            parts[(row + drow, col + dcol)]
            for (drow, dcol) in DIRECTIONS
            if parts.get((row + drow, col + dcol), None)
        }
        if len(adjacent_parts) == 2:
            yield functools.reduce(mul, (int(part.group()) for part in adjacent_parts))


def solve_part1(puzzle_input: list[str]) -> int:
    parts = find_parts(puzzle_input)
    symbol_locations = locate_symbols(puzzle_input)
    return sum(
        int(part.group())
        for part in yield_part_if_adjacent(parts, symbol_locations)
    )


def solve_part2(puzzle_input) -> int:
    parts = find_parts(puzzle_input)
    gear_locations = locate_symbols(puzzle_input, {GEAR})
    return sum(
        gear_ratio 
        for gear_ratio in yield_gear_ratio(parts, gear_locations)
    )


if __name__ == '__main__':

    title = 'Day 03: Gear Ratios'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The sum of the part numbers is {part1}.
        Part 2: The sum of the gear ratios is {part2}.
        """)
