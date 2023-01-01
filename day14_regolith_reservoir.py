"""
--- Day 14: Regolith Reservoir ---
"""
import itertools
import collections
from typing import Iterable, Iterator
import enum

import numpy as np


Point = collections.namedtuple('Point', ['x', 'y'])


def draw_segment(start: Point, end: Point) -> tuple:
    """
    Draw a line segment from start to end by returning the
    arrays of x indices and y indices.
    For example, draw_segment(point(0,0), point(2,0)) would return
    (array([0, 1]), array([0, 0])) because the segment would pass through
    points (0, 0), (1,0), and (2,0).
    """
    right = int((end.x - start.x) / abs(end.x - start.x)) if abs(end.x - start.x) > 0 else 0
    down = int((end.y - start.y) / abs(end.y - start.y)) if abs(end.y - start.y) > 0 else 0
    x_indices = np.array([x for x in range(start.x, end.x + right * 1, right)]) \
        if right != 0 else \
        np.array([start.x for _ in range(start.y, end.y + down * 1, down)])
    y_indices = np.array([y for y in range(start.y, end.y + down * 1, down)]) \
        if down != 0 else \
        np.array([start.y for _ in range(start.x, end.x + right * 1, right)])
    return x_indices, y_indices


class Path:
    """
    A python class object holding a path.
    """

    def __init__(self, points: Iterator[Point] | Iterable[Point]):
        self.segments = []
        self.points = list(points) if isinstance(points, Iterator) else points

    def __repr__(self):
        rep = ' -> '.join(f"{p.x, p.y}" for p in self.points)
        return f'Path through {rep}'

    def draw_segments(self):
        self.segments.clear()
        for endpoints in itertools.pairwise(self.points):
            self.segments.append(
                draw_segment(*endpoints)
            )


class Cell(enum.IntEnum):
    AIR = 0
    ROCK = 1
    SAND = 2


class gridLocation:

    def __init__(self, **kwargs):
        self.x, self.y = None, None
        self.row, self.column = None, None
        if 'x' in kwargs and 'y' in kwargs:
            self.x, self.y = kwargs['x'], kwargs['y']
        if 'row' in kwargs and 'column' in kwargs:
            self.row, self.column = kwargs['row'], kwargs['column']

def minmax(iterable, **kwargs):
    """
    Return minimum and maximum of input iterable.
    """
    my_list = list(iterable)  # to iterate over iterators twice
    MinMax = collections.namedtuple('minmax', ['min', 'max'])
    if not my_list:
        if 'default' in kwargs:
            return (kwargs['default'], kwargs['default'])
        else:
            raise ValueError('minmax is an empty iterable')
    else:
        return MinMax(
            min=min(my_list, key=kwargs.get('key', None)),
            max=max(my_list, key=kwargs.get('key', None))
        )


class GridMatrix:
    """
    A class holding grid-matrix data and
    sand unit movement.
    """
    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self._grid = np.full(
            shape=(
                abs(ymax - ymin) + 1,
                abs(xmax - xmin) + 1
            ),
            fill_value=Cell.AIR
        )
        self._source = gridLocation(
            x=500, y=0,
            row=0, column=500-self.xmin
        )

    def map_paths(self, paths: list[Path]):
        """
        Map rock paths on the grid.
        """
        for path in paths:
            for segment in path.segments:
                x_indices, y_indices = segment
                i_indices, j_indices = y_indices, x_indices - self.xmin
                self._grid[i_indices, j_indices] = Cell.ROCK

    def blocked(self, loc: gridLocation) -> bool:
        """A location is blocked if its cell is not filled with AIR."""
        return self._grid[loc.row, loc.column] != Cell.AIR

    def sand_rest(self, loc: gridLocation):
        """
        Block the cell location on the grid with SAND.
        """
        self._grid[loc.row, loc.column] = Cell.SAND

    def sand_fall(self, current_loc: gridLocation = None):
        """
        Sand unit will fall into the next unblocked cell in the following order:
        - the cell directly below,
        - the cell to the lower left, or
        - the cell to the lower right.
        If all three locations are blocked, rest the sand unit.
        """
        if current_loc is None:
            current_loc = self._source

        direct_below = gridLocation(row=current_loc.row + 1, column=current_loc.column)
        left_diag = gridLocation(row=current_loc.row + 1, column=current_loc.column - 1)
        right_diag = gridLocation(row=current_loc.row + 1, column=current_loc.column + 1)

        if not self.blocked(direct_below):
            return self.sand_fall(direct_below)
        elif not self.blocked(left_diag):
            return self.sand_fall(left_diag)
        elif not self.blocked(right_diag):
            return self.sand_fall(right_diag)
        else:
            return self.sand_rest(current_loc)


with open('day14_input.txt', 'r') as f:
    paths = [
        Path(
            Point(
                int(coord.split(',')[0]),
                int(coord.split(',')[1])
            )
            for coord in line.strip().split(' -> ')
        )
        for line in f
    ]
for path in paths:
    path.draw_segments()

xmin, xmax = minmax(
    map(lambda coord: coord.x, (point for path in paths for point in path.points))
)
ymin, ymax = minmax(
    map(lambda coord: coord.y, (point for path in paths for point in path.points))
)
xmin, xmax = min(500, xmin), max(500, xmax)
ymin, ymax = min(0, ymin), max(0, ymax)


g = GridMatrix(xmin, xmax, ymin, ymax)
g.map_paths(paths)
for count in itertools.count():
    try:
        g.sand_fall()
    except IndexError:
        break
print(count)



