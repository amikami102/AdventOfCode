"""
-- Day 23: Unstable Diffusion --

Inspired by
    - (Peter Norvig's solution)
    https://colab.research.google.com/github/norvig/pytudes/blob/main/ipynb/Advent-2022.ipynb#scrollTo=X7XYM8aji_oO
"""
from typing import *
import collections
import functools
import itertools

Point = collections.namedtuple('Point', ['x', 'y'])

orthogonals = East, South, West, North = (0, 1), (1, 0), (0, -1), (-1, 0)
diagonals = NE, NW, SE, SW = (-1, 1), (-1, -1), (1, 1), (1, -1)
directions8 = orthogonals + diagonals

GROUND, ELF = '.', '#'

proposal_rules = [
    [North, NE, NW],
    [South, SE, SW],
    [West, NW, SW],
    [East, NE, SE]
]


class Grid(collections.defaultdict):
    """ A 2d grid represented as a mapping of {(x, y): cell_value} """
    def __init__(self, grid: list[str], default: str, directions: Iterable):
        """Initialize with Grid(['...###.', '...####']) """
        super().__init__()
        self.default = default
        self.directions = directions
        self.update(
            {
                Point(x, y): value
                for x, line in enumerate(grid)
                for y, value in enumerate(line)
            }
        )

    def __missing__(self, key):
        return self.default

    def get_neighbors(self, point: Point) -> Iterator[str]:
        return (
            self.get(Point(point.x + dx, point.y + dy), self.default)
            for (dx, dy) in self.directions
        )


def elves_make_proposals(current_grid: Grid, current_rules: collections.deque) -> dict:
    """
    Create a dictionary mapping a point on the grid and the elves that want to move there.
    """
    proposals = collections.defaultdict(list)

    def is_valid(three_directions: list[tuple[int, int], ...], elf: Point) -> bool:
        """
        Check whether the elf can move in one of the directions to try
        given the current grid layout.
        """
        return not any(
            current_grid.get(
                Point(elf.x + dx, elf.y + dy), current_grid.default
            ) == ELF
            for (dx, dy) in three_directions
        )
    for point, cell in current_grid.items():
        if cell == ELF and ELF in current_grid.get_neighbors(point):
            is_valid_ground = functools.partial(is_valid, elf=point)
            valid_direction = next(filter(is_valid_ground, current_rules), None)
            if valid_direction:
                x, y = valid_direction[0]
                proposals[Point(point.x + x, point.y + y)].append(point)
    return proposals


def diffuse_n_rounds(grid: Grid, n: int) -> Grid:
    """
    Simulate elf diffusion over n rounds.
    """
    current_rules = collections.deque(proposal_rules)
    for _ in range(n):
        for loc, elves in elves_make_proposals(grid, current_rules).items():
            if len(elves) == 1:
                grid[loc], grid[elves[0]] = ELF, GROUND
        current_rules.rotate(-1)
    return grid


def count_ground(grid: Grid) -> int:
    """Count the number of GROUND cells in the smallest rectangle containing all the elves"""
    def minmax(iterator: Iterator) -> tuple:
        iterable = list(iterator)
        MinMax = collections.namedtuple('MinMax', ['Min', 'Max'])
        return MinMax(min(iterable), max(iterable))
    elves = {point for point in grid.keys() if grid[point] == ELF}
    x0, x1 = minmax(x for x, _ in elves)
    y0, y1 = minmax(y for _, y in elves)
    return (y1 - y0 + 1) * (x1 - x0 + 1) - len(elves)


with open('day23_input.txt', 'r') as f:
    ground = Grid(grid=f.read().splitlines(), default=GROUND, directions=directions8)
n = 10
part1 = count_ground(diffuse_n_rounds(ground, n))
print(f'Part 1: After {n} rounds, there are {part1} ground spaces.')    # 3780


def diffuse(grid: Grid) -> Iterator[Grid]:
    """
    Diffuse elves until none of them can move anymore.
    """
    current_rules = collections.deque(proposal_rules)
    yield grid
    while True:
        moves = {
            loc: elves[0]
            for loc, elves in elves_make_proposals(grid, current_rules).items()
            if len(elves) == 1
        }
        if not moves:
            return
        else:
            for loc, elf in moves.items():
                grid[loc], grid[elf] = ELF, GROUND
        current_rules.rotate(-1)
        yield grid


with open('day23_input.txt', 'r') as f:
    ground = Grid(grid=f.read().splitlines(), default=GROUND, directions=directions8)
part2 = sum(1 for _ in diffuse(ground))
print(f'Part 2: Elves keep moving until round {part2}.')    # 930