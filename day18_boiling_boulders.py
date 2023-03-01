"""
-- Day 18: Boiling Boulders --

Usage example
    Advent_of_Code/year2022 $ python day18_boiling_boulders.py day18_test.txt day18_input.txt

Inspired by Peter Norvig' solution for its parsimony
(cf. https://www.reddit.com/r/adventofcode/comments/zoqhvy/comment/j1ry942/?utm_source=share&utm_medium=web2x&context=3).
"""
import sys
import collections
import pathlib
from typing import *

Voxel = collections.namedtuple('Voxel', ['x', 'y', 'z'])


def _get_adjacent_voxels(voxel: Voxel) -> Iterator[Voxel]:
    """
    Yield a voxel that would be adjacent to the input voxel
    """""
    shifts = [
        (1, 0, 0),      # shift by 1 unit on x-axis
        (0, 1, 0),      # shift by 1 unit on y-axis
        (0, 0, 1),      # shift by 1 unit on z-axis
        (-1, 0, 0),     # shift by -1 unit on x-axis
        (0, -1, 0),     # shift by -1 unit on y-axis
        (0, 0, -1)      # shift by -1 unit on z-axis
    ]
    for shift in shifts:
        yield Voxel(*tuple(p + q for p, q in zip(voxel, shift)))


def _count_surface_area(voxels: list[Voxel]) -> int:
    """
    Count the surface area of input voxels by iterating over
    the input list and counting the adjacent voxels that are not listed in the input.
    """
    return sum(
        1
        for voxel in voxels
        for neighbor_voxel in _get_adjacent_voxels(voxel)
        if neighbor_voxel not in voxels
    )


def _count_exterior_surface_area(voxels: list[Voxel]):
    """
    Count the surface area of input voxels by breadth-first search of
    voxels adjacent to but not included in the input voxels.
    The exteriorty is guaranteed by
        a) starting on a voxel adjacent to an exterior voxel and
        b) not adding input voxel into frontier queue.
    """
    cnt: int = 0

    def _minmax(iterable: Iterable) -> tuple[int, int]:
        MinMax = collections.namedtuple('MinMax', ['min', 'max'])
        my_list = list(iterable)
        return MinMax(min(my_list), max(my_list))

    xmin, xmax = _minmax(voxel.x for voxel in voxels)
    ymin, ymax = _minmax(voxel.y for voxel in voxels)
    zmin, zmax = _minmax(voxel.z for voxel in voxels)

    def _is_proximate(voxel: Voxel) -> bool:
        return xmin - 1 <= voxel.x <= xmax + 1 and\
            ymin - 1 <= voxel.y <= ymax + 1 and\
            zmin - 1 <= voxel.z <= zmax + 1

    initial: Voxel = Voxel(xmin - 1, ymin - 1, zmin - 1)

    frontier: collections.deque[Voxel] = collections.deque([initial])
    explored: set[Voxel] = {initial}

    while frontier:
        for p in _get_adjacent_voxels(frontier.pop()):
            if p in voxels:     # touched a surface of input voxels
                cnt += 1
            elif _is_proximate(p) and p not in explored:
                frontier.append(p)
                explored.add(p)
    return cnt


def parse(txt_filename) -> list[Voxel]:
    """Return the file content as a list of Voxels."""
    return [
        Voxel(*tuple(map(int, line.split(','))))
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


solve_part1 = _count_surface_area
solve_part2 = _count_exterior_surface_area

if __name__ == '__main__':
    title = 'Day 18: Boiling Boulders'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        print(f"""{path}""")
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(part1, part2)
