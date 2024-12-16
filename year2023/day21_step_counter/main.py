"""
Like Day 20, part 2 required peaking at the puzzle input.
Here are some key observations.
    - The grid is a 131 x 131 square.
    - The 'S' plot is placed exactly in the middle at coordinate (65, 65).
    - The garden plot tiles that can be reached at each step count are 
        shaped like a diamond.
    - The first time the aforementioned diamond touches an outer edge of
        garden map is at step count 65. In fact, each corner of the 
        diamond touch an edge of the garden map like this:
        +-------+
        |   +   |
        | +   + |
        |+  S  +|
        | +   + |
        |   +   |
        +-------+
    - The next time the aforementioned diamond corners touch 
        outer garden edges is 65 + 131 steps when
        there is one more map extended in 
        all eight directions from the original map (denoted with S) like this:
        | 1 | 1 | 1 |
        | 1 | S | 1 |
        | 1 | 1 | 1 |
    - The target step count is 
        26_501_365 = 65 + 131 * 202_300.

Let t(n) be the number of tiles reached after crossing n maps in a single 
direction after the first map.
    - t(0) = the number of tiles reached after 65 + 131 * 0 steps
    - t(1) = the number of tiles reached after 65 + 131 * 1 steps
    ... 
    - t(202_300) = the number of tiles reached after 
        65 + 131 * 202_300 =  26_501_365 steps

Some Reddit sleuthing reveals that t(n) is a quadratic sequence:
    t(n) = a * n^2 + b * n + c.
Extrapolating a sequence like this can be done with difference tables.
See https://thirdspacelearning.com/gcse-maths/algebra/quadratic-sequences/,
accessed 2024-01-16.
"""
import sys
from pathlib import Path
from enum import Enum
from collections import UserDict
from typing import Iterator
from itertools import pairwise


ROW, COLUMN = 0, 1
DIRECTIONS = NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)


class GardenPlot(Enum):
    START = 'S'
    PLOT = '.'
    ROCK = '#'


Coordinate = tuple[int, int]


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    row1, col1 = coord1
    row2, col2 = coord2
    return row1 + row2, col1 + col2


class Grid(UserDict):
    """A 2D grid mapped as {(row, column): cell}"""
    def __init__(self, grid: list[str]):
        self.size = len(grid), max(len(row) for row in grid)
        super().__init__(
            {
                (row, column): GardenPlot(cell)
                for row, line in enumerate(grid)
                for column, cell in enumerate(line)
            }
        )
    
    def __missing__(self, nonexistent_key: Coordinate) -> str:
        row, column = nonexistent_key
        nrow, ncol = self.size
        return self[(row % nrow, column % ncol)]
    
    def findall(self, cell_content: str) -> Iterator[Coordinate]:
        for coordinate in self:
            if self[coordinate] == cell_content:
                yield coordinate

    def neighbors(self, current: Coordinate) -> Iterator[Coordinate]:
        for direction in DIRECTIONS:
            yield add_coordinates(current, direction)


def take_steps(garden: Grid, size: int) -> set[Coordinate]:
    """(Part 1)
    Return the locations in `garden` that can be reached in `size` steps.
    """
    rocks: set[Coordinate] = set(garden.findall(GardenPlot.ROCK))
    locations: Iterator[Coordinate] = garden.findall(GardenPlot.START)
    for _ in range(size):
        locations: set[Coordinate] = {
            neighbor
            for location in locations
            for neighbor in garden.neighbors(location)
        } - rocks
    return locations


def take_steps_infinitely(garden: Grid, n: int) -> set[Coordinate]:
    """(Part 2)
    Return the number of tiles reached if you can take `n` steps 
    when `garden` extends infinitely.
    """
    rocks: set[Coordinate] = set(garden.findall(GardenPlot.ROCK))
    locations: Iterator[Coordinate] = garden.findall(GardenPlot.START)
    for _ in range(n):
        next_locations: set[Coordinate] = {
            neighbor
            for location in locations
            for neighbor in garden.neighbors(location)
        } 
        rocks.update(
            {
                location
                for location in (next_locations - set(locations))
                if garden[location] is GardenPlot.ROCK
            }
        )
        locations = next_locations - rocks
    return locations


def extrapolate_quadratic_sequence(x: int, a: int, b: int, c: int) -> int:
    """(Part 2)"""
    return int(a * (x ** 2) + b * x + c)


def generalize_from_sample(*sample) -> tuple[int, int, int]:
    """(Part 2) 
    Given a data sample {(x, f(x)} = {(0, t0), (1, t1), (2, t2)},
    find the constant coefficients of a quadratic sequence,
        f(x) = a * x^2 + b*x + c.
    """
    f0, f1, *_ = sample
    first_differences: list[int] = [
        second - first 
        for first, second in pairwise(sample)
    ]
    second_difference: int = max(first_differences) - min(first_differences)
    c = f0
    a = second_difference // 2
    b = f1 - a - c
    return a, b, c
    

def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input, *args) -> int:
    garden = Grid(puzzle_input)
    return len(take_steps(garden, *args))


def solve_part2(puzzle_input) -> int:
    garden = Grid(puzzle_input)
    target_steps = 26_501_365
    data = tuple(
        len(take_steps_infinitely(garden, 65 + 131 * x))
        for x in range(3)
    )
    return extrapolate_quadratic_sequence(
        (target_steps - 65) // 131, *generalize_from_sample(*data)
    )

    
if __name__ == '__main__':

    title = 'Day 21: Step counter'
    print(title.center(50, '-'))


    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        if txtfile == 'test.txt':
            assert solve_part1(data, 1) == 2
            assert solve_part1(data, 2) == 4
            assert solve_part1(data, 3) == 6
            assert solve_part1(data, 6) == 16
        part1 = solve_part1(data, 64)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The number of garden plots reached at the 64-th step is {part1}.
        Part 2: The number of garden plots reached at the 26501365-th step is {part2}.
        """)
