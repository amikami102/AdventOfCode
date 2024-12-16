import sys
from pathlib import Path
from collections import UserDict
from typing import Iterable, Iterator
from itertools import combinations

ROW, COLUMN = 0, 1
SPACE = '.'
GALAXY = '#'


Coordinate = tuple[int, int]
Vector = Coordinate


def manhattan_distance(coord1: Coordinate, coord2: Coordinate) -> int:
    row1, col1 = coord1
    row2, col2 = coord2
    return abs(row1 - row2) + abs(col1 - col2)


def get_range(*integers) -> range:
    """Return the `range` object that would cover `integers`."""
    return range(min(integers), max(integers) + 1)


class Grid(UserDict):
    """A 2D grid whose data is stored as {(row, col): cell}"""

    def __init__(self, grid: list[str]):
        super().__init__(
            {
                (row, column): cell
                for row, line in enumerate(grid)
                for column, cell in enumerate(line)
            }
        )
    
    def findall(self, cell_type: set[str]) -> Iterable[Coordinate]:
        return [coord for coord in self if self[coord] in cell_type]


def intergalactic_distances(universe: Grid, expansion_factor: int = 2) -> Iterator[int]:
    """
    Iteratively yield intergalactic distances.
    First, find the galaxy coordinates.
    For every pair of galaxies, 
        1. find the Manhattan distance;
        2. find the number of row coordinates between the galaxies without galaxy 
        (factored by `expansion_factor`, which defaults to 1);
        3. find the number of column coordinates between the galaxies without galaxy;
        4. add up the distances found in steps 2 and 3 and multiply by `expansion_factor` minus 1;
        5. add the Manhattan distance to the sum from step 4.
    """
    galaxies = universe.findall({GALAXY})
    rows_with_galaxies = {galaxy[ROW] for galaxy in galaxies}
    columns_with_galaxies = {galaxy[COLUMN] for galaxy in galaxies}
    for galaxy1, galaxy2 in combinations(galaxies, 2):
        distance_pre_expansion = manhattan_distance(galaxy1, galaxy2)
        horizontal_expansion = len(
            set(get_range(galaxy1[COLUMN], galaxy2[COLUMN])) - columns_with_galaxies
        ) 
        vertical_expansion = len(
            set(get_range(galaxy1[ROW], galaxy2[ROW])) - rows_with_galaxies
        )
        yield distance_pre_expansion + \
            (horizontal_expansion + vertical_expansion) * (expansion_factor - 1)


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    universe = Grid(puzzle_input)
    return sum(distance for distance in intergalactic_distances(universe))
    

def solve_part2(puzzle_input: list[str], **kwargs) -> int:
    universe = Grid(puzzle_input)
    return sum(
        distance
        for distance in intergalactic_distances(universe, **kwargs)
    )


if __name__ == '__main__':

    title = 'Day 11: Cosmic expansion'
    print(title.center(50, '-'))

    for filename in sys.argv[1:]:
        data = parse(filename)
        part1 = solve_part1(data)
        if filename == 'test.txt':
            assert solve_part2(data, expansion_factor=10)   == 1030
            assert solve_part2(data, expansion_factor=100)  == 8410
        part2 = solve_part2(data, expansion_factor=1_000_000)
        print(f"""{filename}
        Part 1: The sum of the inter-galactic distances post-expansion is {part1}.
        Part 2: The sum of the inter-galactic distances post-expansion is {part2}.
        """)
