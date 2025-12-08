# year2025/day04/main.py
from pathlib import Path
from collections import UserDict
from typing import Iterable, Collection, Iterator
from textwrap import dedent

from more_itertools import peekable

Coordinate = Vector = tuple[int, int]

ROW, COLUMN = 0, 1
NSWE = NORTH, SOUTH, WEST, EAST = (1, 0), (-1, 0), (0, -1), (0, 1)
DIAGONALS = NW, NE, SW, SE = (-1, -1), (-1, 1), (1, -1), (1, 1)
EIGHT = NSWE + DIAGONALS

def add_coordinates(
        coord1: Coordinate, 
        coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW],
        coord1[COLUMN] + coord2[COLUMN]
    )

class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to its cell content.
    """
    def __init__(
        self, 
        data: Iterable[Iterable[str]] = (), 
        directions: tuple[Vector, ...] = NSWE):
        grid = {
                (row, column): cell
                for row, line in enumerate(data)
                for column, cell in enumerate(line)
            }
        super().__init__(grid)
        self.directions = directions
    
    def __missing__(self, coordinate: Coordinate):
        return None
    
    def find_cells(self, targets: Collection) -> list[Coordinate]:
        return [
            coord
            for coord in self 
            if self[coord] in targets
        ]
    
    def get_neighbors(
        self, 
        source: Coordinate) -> Iterator[Coordinate]:
        for direction in self.directions:
            if (dst := add_coordinates(source, direction)) in self:
                yield dst
     

def parse(txtfile: str) -> Iterable[str]:
    return Path(txtfile).read_text().splitlines()


def count_rolls_nearby(grid: Grid, cell: Coordinate) -> int:
    return sum(
        grid[adjacent] == '@'
        for adjacent in grid.get_neighbors(cell))


def find_accessible_rolls(grid: Grid) -> Iterator[Coordinate]:
    rolls = grid.find_cells({'@'})
    for roll in rolls:
        if count_rolls_nearby(grid, roll) < 4:
            yield roll


def solve_part1(data: Iterable[str]) -> int:
    grid = Grid(data, directions=EIGHT)
    return len(set(find_accessible_rolls(grid)))


def solve_part2(data: Iterable[str]) -> int:
    grid = Grid(data, directions=EIGHT)
    removed = set()
    while (accessible := peekable(find_accessible_rolls(grid))):
        for location in accessible:
            grid[location] = '.'
            removed.add(location)
    return len(removed)


if __name__ == '__main__':
    print('======== day 04: printing department ========')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""\
        part 1: the number of paper rolls that the forklift can access is {part1}.
        part 2: the number of paper rolls removed is {part2}."""))