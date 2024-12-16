"""
Part 1 solution adapted from Peter Norvig's Advent of Code day 10 solution:
https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2023.ipynb, accessed 2024/01/07.
Part 2 solution inspired by David Brownman's Advent of Code day 10 solution:
https://advent-of-code.xavd.id/writeups/2023/day/10/, accessed 2024/01/08.
"""
import sys
from pathlib import Path
from collections import UserDict
from typing import Sequence
from itertools import pairwise
import math

Coordinate = tuple[int, int]
Vector = Coordinate


ROW, COLUMN = 0, 1
DIRECTIONS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
PIPES = {
    '|' : (UP, DOWN),
    '-' : (LEFT, RIGHT),
    'L' : (UP, RIGHT),
    'J' : (LEFT, UP),
    '7' : (LEFT, DOWN),
    'F' : (DOWN, RIGHT),
    'S' : DIRECTIONS,
    '.' : ()
}


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    """Return a new coordinate that is the sum of `coord1` and `coord2`."""
    row1, col1 = coord1
    row2, col2 = coord2
    return (row1 + row2, col1 + col2)


def reverse(vector: Vector) -> Vector:
    """Reverse `vector` by returning the opposite signs of the components."""
    drow, dcol = vector
    return (-drow, -dcol)


class Grid(UserDict):
    """A 2D grid implemented as a mapping of (row, column) coordinate to cell content."""

    def __init__(self, mapping: list[str]=()):
        grid = {
                (row, column): cell
                for row, line in enumerate(mapping)
                for column, cell in enumerate(line)
            }
        super().__init__(grid)
        self.enclosure: Sequence[Coordinate] = []
    
    def __missing__(self, coordinate: Coordinate):
        return None

    def find_next_pipe(self) -> Coordinate:
        """Find the next connecting pipe of the enclosure in `maze`."""
        current = self.enclosure[-1]
        previous = self.enclosure[-2] if len(self.enclosure) >= 2 else None
        for direction in PIPES[self[current]]:
            candidate = add_coordinates(current, direction)
            if reverse(direction) in PIPES[self[candidate]] and candidate != previous:
                return candidate

    def find_enclosure(self) -> None:
        """
        Find the enclosure starting and ending at 'S' cell in `maze`,
        i.e. if 'S' is at (0, 1), `self.enclosure` will be [(0, 1), ..., (0, 1)].
        """
        start = next(coord for coord in self if self[coord] == 'S')
        self.enclosure = [start]
        while len(self.enclosure) == 1 or self.enclosure[-1] != start:
            self.enclosure.append(self.find_next_pipe())
        

def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    """
    The farthest coordinate from the starting cell is 
    half of the sequence of enclosure loop starting and ending with the starting cell.
    """
    maze = Grid(puzzle_input)
    maze.find_enclosure()
    return len(maze.enclosure) // 2


def solve_part2(puzzle_input) -> int:
    """
    Use shoelace formula to calculate the area inside the pipe loop
    and then use Pick's theorem to count the number of coordinates enclosed.
    """
    maze = Grid(puzzle_input)
    maze.find_enclosure()
    area_inside_enclosure = abs(
        sum(
            row1 * col2 - row2 * col1
            for (row1, col1), (row2, col2) in pairwise(maze.enclosure)
        ) / 2
    )
    return math.ceil(
        area_inside_enclosure + 1 - (len(maze.enclosure) / 2)
    )


if __name__ == '__main__':

    title = 'Day 10: Pipe maze'
    print(title.center(50, '-'))

    for filename in sys.argv[1:]:
        data = parse(filename)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{filename}
        Part 1: The number of steps within the loop farthest from the starting point is {part1}.
        Part 2: The number of enclosed cells is {part2}.
        """)
