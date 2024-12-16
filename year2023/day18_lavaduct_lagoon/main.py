import sys
from pathlib import Path
from collections import namedtuple
from typing import Iterator
import re
from functools import reduce, partial
from itertools import pairwise


Coordinate = tuple[int, int]
Instruction = namedtuple('Instruction', ['direction', 'n'])

ROW, COLUMN = 0, 1
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
TRENCH = '#'
GROUND = '.'
DIRECTIONS = {
    'R': RIGHT, 'L': LEFT, 'U': UP, 'D': DOWN,
    '0': RIGHT, '1': DOWN, '2': LEFT, '3': UP
}
HEXCOLOR_RE = re.compile(r'\(#([a-z0-9]{5})(.)\)')


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    row1, col1 = coord1
    row2, col2 = coord2
    return row1 + row2, col1 + col2


def scalar_multiply(coord: Coordinate, scalar: int) -> Coordinate:
    return coord[ROW] * scalar, coord[COLUMN] * scalar


def dig_terrain(instructions: list[Instruction]) -> Iterator[Coordinate]:
    coord = (0, 0)
    yield coord
    for direction, n in instructions:
        coord = add_coordinates(coord, scalar_multiply(direction, n))
        yield coord


def shoelace_formula(polygon_points: list[Coordinate]) -> float:
    """
    Use shoelace formula to find the number of Cartesian
    points inside a polygon outlined by connecting `polygon_points`.
    """
    return abs(
        sum(
            row1 * col2 - row2 * col1
            for (row1, col1), (row2, col2) in pairwise(polygon_points)
        ) / 2
    )

def picks_theorem(polygon_points: list[Coordinate], boundary_length: int) -> int:
    """
    Use Pick's theorem to calculate the number of interior points
    contained inside a polygon outlined by connecting `polygon_points`
    and the number of points on its boundary (`boundary_length`).
    """
    area = shoelace_formula(polygon_points)
    return int(area + 1 - (boundary_length / 2))


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def parse_instruction(instruction: str, hexadecimal: bool = False) -> Instruction:
    direction, meters, color = instruction.split(' ')
    if not hexadecimal:
        return Instruction(DIRECTIONS[direction], int(meters))
    else:
        meters, direction = HEXCOLOR_RE.match(color).groups()
        return Instruction(DIRECTIONS[direction], int(meters, 16))


def solve(puzzle_input, **kwargs) -> int:
    instructions = [parse_instruction(line, **kwargs) for line in puzzle_input]
    boundary_points = [trench for trench in dig_terrain(instructions)]
    boundary_length = sum(instruction.n for instruction in instructions)
    return picks_theorem(boundary_points, boundary_length) + boundary_length


solve_part1 = solve
solve_part2 = partial(solve, hexadecimal=True)


if __name__ == '__main__':

    title = 'Day 18: Lavaduct lagoon'
    print(title.center(50, '-'))

    assert parse_instruction('R 6 (#70c710)') == Instruction((0, 1), 6)
    assert parse_instruction('R 6 (#70c710)', True) == Instruction((0, 1), 461937)

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The number of trenches dug is {part1}.
        Part 2: The number of trenches dug is {part2}.
        """)
