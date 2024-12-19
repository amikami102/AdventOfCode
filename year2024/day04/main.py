# year2024/day04/main.py
import sys 
from typing import Iterator
from collections import UserDict
from pathlib import Path

Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
NSWE = (0, -1), (0, 1), (-1, 0), (1, 0)
DIAGONALS = NE, SE, NW, SW = (-1, 1), (1, 1), (-1, -1), (1, -1)
DIRECTIONS = (
    *NSWE, *DIAGONALS 
)
CROSSES = [
    (SE, SW),
    (NE, SE),
    (NW, SW),
    (NW, NE)
]

def scale_vector(vector: Vector, scalar: int) -> Vector:
    return (vector[ROW] * scalar, vector[COLUMN] * scalar)


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW], coord1[COLUMN] + coord2[COLUMN]
    )


class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to cell content.
    """

    def __init__(self, data: list[str]=()):
        grid = {
                (row, column): cell
                for row, line in enumerate(data)
                for column, cell in enumerate(line)
            }
        super().__init__(grid)
    
    def __missing__(self, coordinate: Coordinate):
        return None


def parse(txtfile: str) -> list[str]:
    return [
        line.strip()
        for line in Path(txtfile).read_text().splitlines()
    ]


def spell_word(
        grid: Grid, 
        origin: Coordinate, 
        direction: Vector, 
        word: str
    ) -> bool:
    """
    Return True if the grid spells `word` starting at `origin`
    in the direction `direction`.
    """
    return all(
        grid[
            add_coordinates(origin, scale_vector(direction, i))
            ] == letter
        for i, letter in enumerate(word)
    )


def spell_word_in_cross(
        grid: Grid, 
        middle: Coordinate, 
        cross: tuple[Vector, Vector], 
        word: str
    ) -> bool:
    """
    Return True if the grid spells `word` in a cross shape 
    in the directions of `cross`
    centered around the tile located at `middle`.
    e.g 
    M.S     S.M     M.M     S.S
    .A.     .A.     .A.     .A.
    M.S     S.M     S.S     M.M
    """
    diagonal1, diagonal2 = cross
    origin1, origin2 = \
        add_coordinates(middle, scale_vector(diagonal1, -1)),\
        add_coordinates(middle, scale_vector(diagonal2, -1))
    return spell_word(grid, origin1, diagonal1, word) and\
        spell_word(grid, origin2, diagonal2, word)


def solve_part1(data) -> int:
    grid = Grid(data)
    return sum(
        spell_word(grid, tile, direction, 'XMAS')
        for tile in grid
        for direction in DIRECTIONS
    )


def solve_part2(data):
    grid = Grid(data)
    return sum(
        spell_word_in_cross(grid, tile, cross, 'MAS')
        for tile in grid if grid[tile] == 'A'
        for cross in CROSSES
    )
                

if __name__ == '__main__':
    title = 'Day 4: Ceres Search'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of XMASes is {part1}.
        Part 2: The number of X-MASes is {part2}.
        """)