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
Coord = collections.namedtuple('Coord', ['row', 'column'])
Forest = collections.defaultdict[Coord, int]

DIRECTIONS4 = Up, Down, Right, Left = (-1, 0), (1, 0), (0, 1), (0, -1)


def parse(txt_filename: str) -> Forest:
    """
    Parse the lines of integers into a list of Tree objects.
    """
    forest = collections.defaultdict(int)
    for row, line in enumerate(pathlib.Path(txt_filename).read_text().splitlines()):
        for column, height in enumerate(line):
            forest[Coord(row, column)] = int(height)
    return forest


def _move_in_direction(here: Coord, forest: Forest, direction: tuple[int, int]) -> Iterator[Coord]:
    """Starting from here, move in the direction through the forest"""
    drow, dcol = direction
    while True:
        here = Coord(here.row + drow, here.column + dcol)
        if here not in forest:
            return None
        else:
            yield here


def solve_part1(forest: Forest) -> int:
    """
    Count the number of trees that are visible from at least one of the DIRECTIONS4.
    """
    def _is_visible_from_direction(ref_tree: Coord, ref_height: int, direction: tuple[int, int]) -> bool:
        """
        A tree in the forest is visible from a direction if
        all the trees in the line of that direction are shorter than the tree of reference.
        Any tree in line that is taller than the tree of sight will block the reference tree when the forest is viewed from that direction.
        """
        return all(
            ref_height > forest[tree_in_line]
            for tree_in_line in _move_in_direction(ref_tree, forest, direction)
        )

    return len(
        list(
            filter(
                lambda tree: any(
                    _is_visible_from_direction(*tree, direction)
                    for direction in DIRECTIONS4
                ),
                forest.items()
            )
        )
    )


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


def solve_part2(forest: Forest) :
    """
    Return the highest scenic score possible in this forest.
    """

    def _scenic_score(ref_coord: Coord, ref_height: int, direction: tuple[int, int]) -> int:
        """
        Return the scenic score of the tree located at ref_coord.
        A ref_tree can see a tree if the tree is not taller than ref_tree['height'].
        """
        shorter, equal_or_taller = before_and_after(
            lambda tree_in_line: ref_height > forest[tree_in_line],
            _move_in_direction(ref_coord, forest, direction)
        )
        match len(list(shorter)), next(equal_or_taller, None):
            case 0, None:
                return 0
            case 0, last_tree if last_tree:
                return 1 if ref_height <= forest[last_tree] else 0
            case _ as n, None:
                return n
            case _ as n, last_tree if last_tree:
                return n + (1 if ref_height <= forest[last_tree] else 0)

    return max(
        math.prod(_scenic_score(*tree, direction) for direction in DIRECTIONS4)
        for tree in forest.items()
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
