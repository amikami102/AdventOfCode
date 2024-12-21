# year2024/day##/main.py
import sys
from pathlib import Path 
from typing import Collection, Iterator, Callable
from collections import UserDict, defaultdict
from itertools import combinations


Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
EMPTY = '.'


def add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return (
        vector1[ROW] + vector2[ROW], 
        vector1[COLUMN] + vector2[COLUMN]
    )

def multiply_scalar(vector: Vector, scalar: int) -> Vector:
    return (vector[ROW] * scalar, vector[COLUMN] * scalar)


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
    
    def find_cells(self, targets: Collection[str]) -> list[Coordinate]:
        return [
            coord
            for coord in self 
            if self[coord] in targets
        ]

    def draw_line(
            self, start: Coordinate, direction: Vector
        ) -> Iterator[Coordinate]:
        while start in self:
            yield start 
            start = add_vectors(start, direction)


def group_antennae_by_frequency(grid: Grid) -> dict[str, list[Coordinate]]:
    groups = defaultdict(list)
    for antenna, frequency in grid.items():
        if frequency != EMPTY:
            groups[frequency].append(antenna)
    return groups


def locate_antinode_pair(
        antenna1: Coordinate, antenna2: Coordinate, grid: Grid
    ) -> Iterator[Coordinate]:
    """
    Return coordinates of `antenna1`'s and `antenna2`'s antinodes.
    Suppose antenna1 is located at (r1, c1), 
            antenna2 at (r2, c2).
    Antenna1's antinode is located at 
        (r1, c1) + (r1, c1) - (r2, c2) = 2(r1, c1) - (r2, c2).
    Antenna2's antinode is located at 
        (r2, c2) + (r2, c2) - (r1, c1) = 2(r2, c2) - (r1, c1).
    """
    antinode1 = add_vectors(
        multiply_scalar(antenna1, 2), multiply_scalar(antenna2, -1)
    )
    antinode2 = add_vectors(
        multiply_scalar(antenna2, 2), multiply_scalar(antenna1, -1)
    )
    if antinode1 in grid:
        yield antinode1 
    if antinode2 in grid:
        yield antinode2
    
    

def follow_antinode_line(
        antenna1: Coordinate, antenna2: Coordinate, grid: Grid
    ) -> Iterator[Coordinate]:  
    direction1 = add_vectors(antenna1, multiply_scalar(antenna2, -1))
    direction2 = add_vectors(antenna2, multiply_scalar(antenna1, -1))
    yield from grid.draw_line(antenna1, direction1)
    yield from grid.draw_line(antenna2, direction2)


def find_all_antinodes(
        city: Grid, antinode_locator: Callable
    ) -> set[Coordinate]:
    antennae_groups = group_antennae_by_frequency(city)
    return {
        antinode 
        for group in antennae_groups.values()
        for pair in combinations(group, 2)
        for antinode in antinode_locator(*pair, city)
    }


def parse(txtfile) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(data: list[str]) -> int:
    city = Grid(data)
    antinodes = find_all_antinodes(city, locate_antinode_pair)
    return len(antinodes)
    

def solve_part2(data) -> int:
    city = Grid(data)
    antinodes = find_all_antinodes(city, follow_antinode_line)
    return len(antinodes)


if __name__ == '__main__':
    title = 'Day 8: Resonant Collinearity'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of antinodes on the map is {part1}.
        Part 2: The updated number of antinodes is {part2}.
        """)