# year2025/day07/main.py
"""
Solution to part 2 liberally borrowed from 
https://github.com/simonbrahan/aoc2025/blob/fb6301dbab0e952f6152b546901a01dc079abd5b/07/p2.py.
"""
from pathlib import Path
from typing import Iterable, Iterator, Collection, Optional, Mapping
from operator import itemgetter
from collections import UserDict, defaultdict
from functools import cached_property
from itertools import groupby

Coordinate = Vector = tuple[int, int]

ROW, COLUMN = 0, 1
NSWE = NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)
NW, NE, SW, SE = (-1, -1), (-1, 1), (1, -1), (1, 1)
START = 'S'
EMPTY = '.'
SPLITTER = '^'

def add_coordinates(
        coord1: Coordinate, 
        coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW],
        coord1[COLUMN] + coord2[COLUMN]
    )

get_column = itemgetter(COLUMN)
get_row = itemgetter(ROW)

class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to its cell content.
    """
    def __init__(
        self, 
        data: Iterable[Iterable[str]] = (), 
        directions: tuple[Vector, ...] = NSWE,
        grid: Optional[Mapping] = None):
        if not grid:
            grid = {
                (row, column): cell
                for row, line in enumerate(data)
                for column, cell in enumerate(line)
            }
        super().__init__(grid)
        self.directions = directions
    
    def __missing__(self, coordinate: Coordinate):
        return None
    
    def find_cells(self, targets: Collection) -> Iterator[Coordinate]:
        return (
            coord
            for coord in self 
            if self[coord] in targets
        )
    
    def get_neighbors(
        self, 
        source: Coordinate) -> Iterator[Coordinate]:
        for direction in self.directions:
            if (dst := add_coordinates(source, direction)) in self:
                yield dst


def parse(txtfile: str) -> Grid:
    return Grid(
        Path(txtfile).read_text().splitlines())


def will_split_beam(splitter: Coordinate, manifold: Grid):
    left, center, right = \
        itemgetter(0), itemgetter(1), itemgetter(2)
    coords = tuple(
        add_coordinates(splitter, vector) for 
        vector in (NW, NORTH, NE))
    if manifold[left(coords)] == SPLITTER or\
        manifold[right(coords)] == SPLITTER:
        return True
    elif manifold[center(coords)] == START:
        return True
    elif manifold[center(coords)] == SPLITTER:
        return False
    else:
        return will_split_beam(center(coords), manifold)


def solve_part1(data: Grid) -> int:
    splitters = data.find_cells(SPLITTER)
    return sum(
        will_split_beam(splitter, data)
        for splitter in splitters
    )


def propogate(
        timelines: dict[int, int], 
        splitters: Collection[int]) -> dict[int, int]:
    new_timelines = defaultdict(int)
    for loc, count in timelines.items():
        if loc in splitters:
            new_timelines[loc - 1] += count 
            new_timelines[loc + 1] += count
        else:
            new_timelines[loc] += count
    return new_timelines


def solve_part2(data: Grid) -> int:
    splitters_per_row = groupby(
        data.find_cells(SPLITTER),
        key=itemgetter(ROW))
    start = next(data.find_cells(START))

    timelines_per_column = defaultdict(int)
    timelines_per_column[start[COLUMN]] = 1

    for _, splitters in splitters_per_row:
        timelines_per_column = propogate(
            timelines_per_column, 
            set(map(get_column, splitters)))
    
    return sum(timelines_per_column.values())


if __name__ == '__main__':
    print('~~~~~~~~~~~ day 7: laboratories ~~~~~~~~~~~~~')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(f"""
    part 1: the beam will split {part1} times.
    part 2: the beam will end up in {part2} different timelines.
    """)