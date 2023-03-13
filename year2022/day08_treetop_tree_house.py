"""
-- Day 08: Treetop Tree House --

Usage example:
    Advent_Of_Code/year2022 $ python day08_treetop_tree_house.py day08_test.txt day08_input.txt
"""
import sys
import pathlib
import math
import collections
from typing import *

T = TypeVar('T')
Coord = tuple[int, int]  # (row, column)
Vector = Coord

ROW, COLUMN = 0, 1
DIRECTIONS4 = Up, Down, Right, Left = (-1, 0), (1, 0), (0, 1), (0, -1)


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[ROW] + vector2[ROW], vector1[COLUMN] + vector2[COLUMN]


def before_and_after(predicate: Callable[T, bool], it: Iterable[T]) -> tuple[Iterator[T], Iterator[T]]:
    """
    Returns two iterator where the first one contains the first half of iterable until the predicate fails and the second is the rest of the iterable.
    """
    it = iter(it)
    transition = []

    def true_iterator() -> Iterator[T]:
        for elem in it:
            if predicate(elem):
                yield elem
            else:
                transition.append(elem)
                return

    def remainder_iterator() -> Iterator[T]:
        yield from transition
        yield from it

    return true_iterator(), remainder_iterator()


class Grid(dict):

    def __init__(self, grid: list[T],
                 directions: tuple[Vector] = DIRECTIONS4, default: T = KeyError, skip: tuple[T] = ()):
        super().__init__()
        self.directions = directions
        self.default = default
        self.skip = skip
        self.update(
            {
                (row, column): int(height)
                for row, line in enumerate(grid)
                for column, height in enumerate(line)
                if height not in self.skip
            }
        )

    def __missing__(self, key: Coord) -> T:
        if self.default is KeyError:
            raise KeyError(f'{key} not found in grid')
        else:
            return self.default

    def get_neighbors(self, key: Coord, cell_value: bool = False) -> Iterator[Coord | T]:
        if cell_value:
            return (
                _add_vectors(key, direction)
                for direction in self.directions
            )
        else:
            return (
                self[_add_vectors(key, direction)]
                for direction in self.directions
            )


def _tree_line(grid: Grid, tree: Coord, direction: Vector) -> Iterator[Coord]:
    while True:
        tree = _add_vectors(tree, direction)
        if grid.get(tree, None):
            yield tree
        else:
            return


def _is_visible_from_direction(grid: Grid, ref_tree: Coord, ref_height: int, direction: Vector) -> bool:
    """
    A tree in the forest is visible from a direction if
    all the trees in the line of that direction are shorter than the tree of reference.
    Any tree in line that is taller than the tree of sight will block the reference tree when the forest is viewed from that direction.
    """
    return all(
        ref_height > grid[tree_in_line]
        for tree_in_line in _tree_line(grid, ref_tree, direction)
    )


def _scenic_score(grid: Grid, ref_coord: Coord, ref_height: int, direction: Vector) -> int:
    """
    Return the scenic score of the tree located at ref_coord.
    A ref_tree can see a tree if the tree is not taller than ref_tree['height'].
    """
    shorter, equal_or_taller = before_and_after(
        lambda tree: ref_height > grid[tree],
        _tree_line(grid, ref_coord, direction)
    )
    match len(list(shorter)), next(equal_or_taller, None):
        case 0, None:
            return 0
        case 0, last_tree if last_tree:
            return 1 if ref_height <= grid[last_tree] else 0
        case _ as n, None:
            return n
        case _ as n, last_tree if last_tree:
            return n + (1 if ref_height <= grid[last_tree] else 0)


def parse(txt_filename: str) -> list[str]:
    return pathlib.Path(txt_filename).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    """
    Count the number of trees that are visible from at least one of the DIRECTIONS4.
    """
    grid = Grid(puzzle_input)
    return len(
        list(
            filter(
                lambda treedata: any(
                    _is_visible_from_direction(grid, *treedata, direction)
                    for direction in DIRECTIONS4
                ),
                grid.items()
            )
        )
    )


def solve_part2(puzzle_input: list[str]) -> int:
    """
    Return the highest scenic score possible in this forest.
    """
    grid = Grid(puzzle_input)
    return max(
        math.prod(
            _scenic_score(grid, *tree, direction)
            for direction in DIRECTIONS4
        )
        for tree in grid.items()
    )


if __name__ == '__main__':
    title = 'Day 08: Treetop Tree House'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The number of trees visible from outside the grid are {part1}.
        Part 2: The highest scenic score in this forest grid is {part2}.
        """)
