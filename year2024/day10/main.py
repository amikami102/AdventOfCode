# year2024/day10/main.py
import sys
from pathlib import Path 
from typing import Collection, Iterator, Iterable, Any
from collections import UserDict, Counter


Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
NSWE = NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)
HEAD = '0'


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW], coord1[COLUMN] + coord2[COLUMN]
    )


def add_up_counts(tallies: Iterable[tuple[Any, int]]) -> Counter[Any, int]:
    counter = Counter()
    for item, count in tallies:
        counter[item] += count 
    return counter 


class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to cell content.
    """

    def __init__(self, data: list[str]=(), directions: tuple[Vector, ...]=NSWE):
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
    
    def get_neighbors(self, source: Coordinate) -> Iterator[Coordinate]:
        for direction in self.directions:
            if (destination := add_coordinates(source, direction)) in self:
                yield destination


def hike(terrain: Grid, trailhead: Coordinate) -> dict[Coordinate, int]:
    """
    Hike the terrain starting from `trailhead` and return a dictionary that 
    maps the coordinate of the trail ends with the number of distinct paths to it. 
    """
    frontier = Counter([trailhead])
    for elevation in range(1, 10):
        frontier = add_up_counts(
            (neighbor, frontier[point])
            for point in frontier
            for neighbor in terrain.get_neighbors(point)
            if terrain[neighbor] == str(elevation)
        )
    return frontier 


def parse(txtfile: str) -> list[list[str]]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(data: list[list[str]]) -> int:
    island = Grid(data)
    heads = island.find_cells(HEAD)
    scorecard = [len(hike(island, head)) for head in heads]
    return sum(scorecard)


def solve_part2(data):
    island = Grid(data)
    heads = island.find_cells(HEAD)
    ratings = [
        count
        for head in heads
        for tail, count in hike(island, head).items()
    ] 
    return sum(ratings)


if __name__ == '__main__':
    title = 'Day 10: Hoof It'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The sum of the scores is {part1}.
        Part 2: The sum of the ratings is {part2}.
        """)