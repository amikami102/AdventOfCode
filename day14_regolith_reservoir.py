"""
-- Day 14: Regolith Reservoir --

Usage example:
    Advent_Of_Code/year2022 $ python day14_regolith_reservoir.py day14_test.txt day14_input.txt

A tricky aspect of grids in Advent of Code is that sometimes the navigation is physical, (row, column), while others it's Cartesian, (x, y), which is what Day 14 uses. However, the y is inverted axis where y increases as you go "down" instead of "up."

Inspired by Peter Norvig's solution to only add grid coordinate to the Grid dictionary if the cell value is either a rock ('#') or a sand particle that has come to rest ('o').
"""
import sys
from typing import *
import collections
import itertools
import pathlib
import enum

Coord = tuple[int, int]     # (x, y), not (row, column)
Vector = Coord
RockPath = list[Coord]

DIRECTIONS = Down, DownLeft, DownRight = (0, 1), (-1, 1), (1, 1)
Source = (500, 0)
ROCK, SAND = '#', 'o'


def _add_vectors(vector0: Vector, vector1: Vector) -> Vector:
    return vector0[0] + vector1[0], vector0[1] + vector1[1]


class Grid(dict):

    def __init__(self, directions: Iterable[Vector], default: str = KeyError) -> None:
        super().__init__()
        self.default = default
        self.directions = directions

    def __missing__(self, key: Coord):
        if self.default == KeyError:
            raise KeyError(f'{key} out of grid index')
        else:
            return self.default


def parse(txt_filename: str) -> list[RockPath]:
    """
    Each line of the file is a path represented by tuple -> tuple -> ....
    """
    return [
        [
            (int(p.split(',')[0]), int(p.split(',')[1]))
            for p in line.split(' -> ')
        ]
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


def _place_rocks(grid: Grid, paths: list[RockPath]) -> Grid:
    """
    Place the paths of rocks on the grid.
    """
    for path_of_rocks in paths:
        for (row0, col0), (row1, col1) in itertools.pairwise(path_of_rocks):
            row_endpoints, col_endpoints = (row0, row1), (col0, col1)
            for coord in itertools.product(
                    range(min(row_endpoints), max(row_endpoints) + 1),
                    range(min(col_endpoints), max(col_endpoints) + 1)
            ):
                grid[coord] = ROCK
    return grid


def _simulate(grid: Grid, lay_floor: bool = False):
    """
    Simulate sand falling from Source until it hits the bottom floor of the grid
    """
    bottom = max(map(lambda coord: coord[1], grid))
    if lay_floor:
        bottom = bottom + 2
        x_left, x_right = Source[0] - bottom, Source[0] + bottom
        grid = _place_rocks(grid, [[(x_left, bottom), (x_right, bottom)]])
    for count in itertools.count(start=1):
        # particles enter from the Source
        loc: Coord = Source
        while True:
            next_fall_locs = [
                _add_vectors(loc, d)
                for d in grid.directions if _add_vectors(loc, d) not in grid
            ]
            new_loc = next(iter(next_fall_locs), loc)
            if new_loc == Source:   # block the source
                return count
            if new_loc == loc:
                grid[new_loc] = SAND
                break  # this particle has come to rest
            elif new_loc[1] > bottom:
                return count - 1    # stop counting before the particle falls into abyss
            loc = new_loc


def solve_part1(puzzle_input: list[RockPath]) -> int:
    """
    Place the rocks on the paths by feeding the puzzle_input into _place_rocks().
    Simulate the sand falling by running _simulate() on default args.
    """
    grid = _place_rocks(Grid(directions=DIRECTIONS), puzzle_input)
    return _simulate(grid)


def solve_part2(puzzle_input: list[RockPath]) -> int:
    """
    The same as part 1, but run _simulate() with the argument lay_floor set to False.
    """
    grid = _place_rocks(Grid(directions=DIRECTIONS), puzzle_input)
    return _simulate(grid, lay_floor=True)


if __name__ == '__main__':
    title = 'Day 14: Regolith Reservoir'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The number of sand particles that come to rest until it starts to fall off into the abyss is {part1}.
        Part 2: The number of sand particles that come to rest until the last one blocks the sand source is {part2}.
        """)
