# year2024/day06/main.py
import sys
from pathlib import Path 
from typing import Collection, Iterator
from collections import UserDict


Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
LEFT, RIGHT, UP, DOWN = (0, -1), (0, 1), (-1, 0), (1, 0)
OBSTRUCTION = '#'
EMPTY = '.'
DIRECTION_LEGEND = {'^': UP , 'v': DOWN, '<': LEFT, '>': RIGHT}
RIGHT_TURNS = {
    LEFT: UP, 
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT
}


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
    
    def find_cells(self, targets: Collection[str]) -> list[Coordinate]:
        return [
            coord
            for coord in self 
            if self[coord] in targets
        ]


def get_starting_position_and_direction(grid: Grid) -> tuple[Coordinate, Vector]:
    position = grid.find_cells(DIRECTION_LEGEND)[0]
    direction = DIRECTION_LEGEND[grid[position]]
    return position, direction


def walk_off_grid(grid: Grid, start: Coordinate, facing: Vector) -> list[Coordinate]:
    """
    Return the list of coordinates that charts the path 
    that starts at `start` in the direction `facing`.
    """
    course = [start]
    while (end := add_coordinates(start, facing)) in grid:
        if grid[end] == OBSTRUCTION:
            facing = RIGHT_TURNS[facing]
        else:
            course.append(end)
            start = end
    return course


def is_course_loop(grid: Grid, start: Coordinate, facing: Vector) -> bool:
    """
    Return True if the course that starts at `start` in the direction `facing`
    results in a closed loop, or a square to be precise.

    The course is a loop if we end up in the same turning corner and turn in the
    same direction as before. Therefore, we only keep track of the corners.
    """
    corners = {(start, facing)}
    while (end := add_coordinates(start, facing)) in grid:
        if grid[end] == OBSTRUCTION:
            facing = RIGHT_TURNS[facing]
            if (end, facing) in corners:
                return True 
            else:
                corners.add((end, facing))
        else:
            start = end
    return False


def yield_tiles_to_block(grid: Grid, start: Coordinate, facing: Vector) -> Iterator[Coordinate]:
    """
    Yield positions from the original course that would create a loop. 
    """
    candidates = set(walk_off_grid(grid, start, facing)) - {start}
    for candidate in candidates:
        grid[candidate] = OBSTRUCTION 
        if is_course_loop(grid, start, facing):
            yield candidate 
        grid[candidate] = EMPTY


def parse(txtfile) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(data) -> int:
    """Find the number of distinct grid tiles visited by the guard."""
    floor_grid = Grid(data)
    source, facing = get_starting_position_and_direction(floor_grid)
    course = walk_off_grid(floor_grid, source, facing)
    return len(set(course))
        

def solve_part2(data):
    """
    Find the number of grid tiles where an obstruction can be placed
    to create a looped path.
    """
    floor_grid = Grid(data)
    source, facing = get_starting_position_and_direction(floor_grid)
    return sum(
        1 if tile is not None else 0 
        for tile in yield_tiles_to_block(floor_grid, source, facing)
    )


if __name__ == '__main__':
    title = 'Day 6: Guard Gallivant'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of distinct positions that guard will visit is {part1}.
        Part 2: The number of candidates that can be placed with an obstruction is {part2}.
        """)