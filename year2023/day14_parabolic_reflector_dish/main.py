"""
The solution for part 2 adapted from Peter Norvig's code:
https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2023.ipynb, accesed 2023-01-11.
"""
import sys
from pathlib import Path
from typing import Iterator
from collections import UserDict
from operator import itemgetter
from itertools import count

Coordinate = tuple[int, int]
Vector = Coordinate


ROW, COLUMN = 0, 1
ROUND = 'O'
CUBE  = '#'
EMPTY = '.'
NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    row1, col1 = coord1
    row2, col2 = coord2
    return row1 + row2, col1 + col2


class Grid(UserDict):
    """A 2D grid represented as {(row, column): cell}"""

    def __init__(self, grid: list[str], skip: set[str]):
        mapping = {
            (row, column): cell
            for row, line in enumerate(grid)
            for column, cell in enumerate(line)
            if cell not in skip
        }
        self.size = len(grid), max(len(row) for row in grid)
        super().__init__(mapping)
    
    def __missing__(self, nonexistent_coordinate: Coordinate) -> None:
        return None
    
    def findall(self, cell_type: str) -> Iterator[Coordinate]:
        for coord in self:
            if self[coord] == cell_type:
                yield coord
    
    def fits(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate[ROW] < self.size[ROW] and\
            0 <= coordinate[COLUMN] < self.size[COLUMN]


def tilt(platform: Grid, direction: Vector = NORTH) -> None:
    """
    Tilt `platform` in `direction` and slide the ROUND rocks as far as they can go.
    Return the new platform after all the round rocks have rolled down.
    """
    sort_keys = {
        NORTH   : {'key': itemgetter(ROW)},
        SOUTH   : {'key': itemgetter(ROW), 'reverse': True},
        WEST    : {'key': itemgetter(COLUMN)},
        EAST    : {'key': itemgetter(COLUMN), 'reverse': True}
    }
    sorted_rocks = sorted(platform.findall(ROUND), **sort_keys[direction])
    for rock in sorted_rocks:
        platform.pop(rock)
        rock = slide(rock, platform, direction)
        platform.update({rock: ROUND})
    

def slide(old_position: Coordinate, platform: Grid, direction: Vector):
    """Slide the rock from `old_position` one unit in `direction` across `platform`."""
    new_position = add_coordinates(old_position, direction)
    while new_position not in platform and platform.fits(new_position):
        old_position, new_position = new_position, add_coordinates(new_position, direction)
    return old_position


def spin(platform: Grid, n: int = 1) -> None:
    """(Part 2)
    Spin the platform by tilting `platform` in 
    a cycle of north, west, south, and then east `n` times.
    """
    for _ in range(n):
        for direction in (NORTH, WEST, SOUTH, EAST):
            tilt(platform, direction)


def find_repeated_cycle(platform: Grid) -> tuple[int, int, Grid]:
    """(Part 2)
    Find how many spins it takes to spin `platform` back to a previously seen state.
    Return the two iterations when the same platform states are observed an the state of the platform.
    """
    history: dict[frozenset[Coordinate], int] = {}
    for step in count():
        rocks = frozenset(platform.findall(ROUND))
        if rocks in history:
            return history[rocks], step, platform
        history[rocks] = step
        spin(platform)


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    platform = Grid(puzzle_input, skip={EMPTY})
    tilt(platform)
    return sum(
        platform.size[ROW] - rock[ROW]
        for rock in platform.findall(ROUND)
    )


def solve_part2(puzzle_input: list[str]) -> int:
    n = 1_000_000_000
    platform = Grid(puzzle_input, skip={EMPTY})
    t1, t2, platform = find_repeated_cycle(platform)
    remaining_cycles = (n - t1) % (t2 - t1)
    spin(platform, remaining_cycles)
    return sum(
        platform.size[ROW] - rock[ROW]
        for rock in platform.findall(ROUND)
    )


if __name__ == '__main__':

    title = 'Day 14: Parabolic reflector dish'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The total load on the north support beams is {part1}.
        Part 2: The total load on the north support beams is {part2}.
        """)
