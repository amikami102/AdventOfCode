"""
-- Day 22: Monkey Map --

Usage example
    Advent_Of_code/year2022 $ python day22_monkey_map.py day22_test.txt day22_input.txt

Part 1 is adapted from Peter Norvig's solution by finding the warp path by walking back.

Part 2 is adapted from this reddit user's solution (https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j1b0fp7/?utm_source=share&utm_medium=web2x&context=3). It finds the warp path beforehand and saves it in a dictionary, which you look up when executing the commands.

Since I wrote a lot of utility functions, the main block executes unit tests with series of `assert` statements.
"""
import sys
import pathlib
import re
import operator
import collections
import itertools
import math
from enum import Enum
from typing import *

Coord = tuple[int, int]     # (row, column)
Vector = Coord
Commands = tuple[str|int]
Edge = collections.namedtuple('Edge', ['coords', 'direction'])  # used in part 2
CubeWrap = dict[tuple[Coord, Vector], tuple[Coord, Vector]]     # used in part 2

ROW, COLUMN = 0, 1
OPEN, WALL, OFF_THE_MAP = '.', '#', ' '


class Directions(Vector, Enum):
    # clockwise order
    UP: Vector = (-1, 0)
    RIGHT: Vector = (0, 1)
    DOWN: Vector = (1, 0)
    LEFT: Vector = (0, -1)


CLOCKWISE_CONCAVE_INTERSECTIONS: dict[Vector, Vector] = {
    Directions.DOWN: Directions.RIGHT,
    Directions.LEFT: Directions.DOWN,
    Directions.UP: Directions.LEFT,
    Directions.RIGHT: Directions.UP
}   # used in part 2


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[ROW] + vector2[ROW], vector1[COLUMN] + vector2[COLUMN]


class Grid(dict):
    """A class object to hold the grid data as a dictionary where the keys are coordinates and values are the tiles (either OPEN or WALL)."""
    def __init__(self, lines: Iterable[str], skip: Iterable[str], directions: list[Vector], default: str = KeyError):
        super().__init__()
        self.skip = skip
        self.directions = directions
        self.default = default
        self.update(
            {
                (row, column): value
                for row, line in enumerate(lines)
                for column, value in enumerate(line)
                if value not in self.skip
            }
        )

    def __missing__(self, key: Coord):
        """Return default cell value or raise KeyError when asked for a key that is not in grid"""
        if self.default is KeyError:
            raise KeyError(f'{key} not in grid')
        else:
            return self.default


def turn(facing: Vector, right: bool = True) -> Vector:
    """
    Return the new direction 90-degrees rotation
    to the right (if right is True) or left (if False) of `facing`.
    """
    idx = list(Directions).index(facing)
    return list(Directions)[(idx + 1) % 4] if right else list(Directions)[(idx - 1) % 4]


def reverse(facing: Vector) -> Vector:
    """Reverse direction so that you turn from Directions.LEFT to Directions.RIGHT, Directions.UP to Directions.DOWN, and vice versa."""
    row, col = facing[ROW], facing[COLUMN]
    return operator.neg(row), operator.neg(col)


def follow_commands(grid: Grid, commands: Commands, on_cube: bool = False) -> tuple[Coord, Vector]:
    """
    Follow the commands and return the final coordinate on Grid and the direction the agent is facing.
    """
    cube: CubeWrap = construct_cubewrap(grid)

    loc: Coord = 0, min(coord[COLUMN] for coord in grid if coord[ROW] == 0)
    facing: Vector = Directions.RIGHT
    for move in commands:
        match move:
            case 'L' | 'R':
                facing = turn(facing) if move == 'R' else turn(facing, False)
            case _ as n:
                if on_cube:
                    loc, facing = move_forward(loc, facing, n, grid, cube)
                else:
                    loc, facing = move_forward(loc, facing, n, grid)
    return loc, facing


def move_forward(loc: Coord, facing: Vector, n: int, grid: Grid, cube: CubeWrap = None) -> Coord:
    """
    Move forward `n` steps in the direction `facing` on `grid` by iterating over range(n).
    Return the final grid coordinate.
    """
    for _ in range(n):
        new_loc, new_facing = _add_vectors(loc, facing), facing
        if new_loc not in grid:     # you're about to walk off the grid
            if not cube:
                new_loc, new_facing = wrap_around_board(loc, facing, grid), facing
            else:
                new_loc, new_facing = wrap_around_cube(loc, facing, cube)
        if grid[new_loc] == WALL:   # you're about to walk onto a WALL tile
            break
        else:
            loc, facing = new_loc, new_facing   # update `loc` and `facing` for next iteration
    return loc, facing


def wrap_around_board(loc: Coord, facing: Vector, grid: Grid) -> Coord:
    """
    Wrapping around the board by walking in the reverse direction to `facing`
    until you get off the grid and returning to the last tile on the grid.

    n.b. Don't worry if the tile returned by the function is a WALL tile.
    This will be checked during `move_forward()`.
    """
    facing_reverse = reverse(facing)  # e.g. Directions.DOWN if facing == Directions.UP, Directions.LEFT if facing == Directions.RIGHT
    while loc in grid:
        loc = _add_vectors(loc, facing_reverse)
    return _add_vectors(loc, facing)


def wrap_around_cube(loc: Coord, facing: Vector, cube: CubeWrap) -> tuple[Coord, Vector]:
    """Look up where (loc, facing) wraps around to when the map is folded into `cube`."""
    return cube[(loc, facing)]


def compute_final_password(loc: Coord, facing: Vector) -> int:
    """Compute the final password which is 1000 * (row index) + 4 * (column index) + (direction index)"""
    return 1000 * (loc[ROW] + 1)\
        + 4 * (loc[COLUMN] + 1)\
        + [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP].index(facing)


def jump_forward_left(loc: Coord, facing: Vector) -> tuple[Coord, Vector]:
    """
    Jump to a coordinate that is 1 step forward in direction `facing`
    and 1 step left of `loc`.
    """
    turn_left = turn(facing, False)
    return _add_vectors(_add_vectors(loc, facing), turn_left), turn_left


def walk_perimeter(grid: Grid) -> Iterator[Edge]:
    """
    Walking around the perimeter of the cube net represented by `grid`;
    during the walk, skip the vertex of reflex angles.
    Yield an Edge object filled with edge coordinates before you're about to turn the corner.
    """
    loc: Coord = (0, min(coord[COLUMN] for coord in grid if coord[ROW] == 0))
    facing: Vector = Directions.RIGHT

    straight_edge = collections.deque()     # container for points on a straight edge

    Start: tuple[Coord, Vector] = (loc, facing)
    walk_completed: bool = False
    while not walk_completed:    # still working around the perimeter
        straight_edge.append(loc)    # add current position to `edge`
        step_forward = _add_vectors(loc, facing)
        jump_loc, turned = jump_forward_left(loc, facing)

        if step_forward not in grid:    # you're about to walk off the grid by moving forward
            yield Edge(direction=facing, coords=tuple(straight_edge))
            straight_edge.clear()
            facing = turn(facing, True)     # turn right to stay on the perimeter
        else:   # you're still walking on the grid if you move forward
            if jump_loc not in grid:    # check that the forward left is off the grid
                loc = step_forward
            else:   # the forward left position is a grid => you're hitting an angle
                yield Edge(direction=facing, coords=tuple(straight_edge))
                straight_edge.clear()
                loc, facing = jump_loc, turned
        walk_completed = (loc, facing) == Start


def identify_cube_sides(grid: Grid) -> list[Edge]:
    """
    Walk around the cube net and return a list of cube sides as instances of Edge.
    """
    contiguous_edges = list(walk_perimeter(grid))
    side_length = math.gcd(*map(lambda edge: len(edge.coords), contiguous_edges))
    return [
        Edge(edge.coords[start: start + side_length], edge.direction)
        for edge in contiguous_edges
        for start in range(0, len(edge.coords), side_length)
    ]


def intersect_concave(idx1: int, idx2: int, angles: list[Vector]) -> bool:
    """
    Check whether `angles[idx1]` and `angles[idx2]` meet at reflex angle of cube net
    assuming that angles are ordered clockwise.
    """
    return CLOCKWISE_CONCAVE_INTERSECTIONS[angles[idx1]] == angles[idx2]


def pair_up_edges(cube_edges: list[Edge]) -> Iterator[tuple[Edge, Edge]]:
    """
    Iterate through the cube edges and yield any pair that form a concave intersection.
    Adjust the directions of remaining cube edges in the iterable.
    """
    leftover, edge_angles = list(range(len(cube_edges))),\
        [edge.direction for edge in cube_edges]

    while leftover:
        (pair0, pair1) = next(
            filter(
                lambda pair: intersect_concave(*pair, angles=edge_angles),
                itertools.pairwise(leftover)
            )
        )
        yield cube_edges[pair0], cube_edges[pair1]
        for idx in leftover:
            if idx > pair1:
                edge_angles[idx] = turn(edge_angles[idx], False)   # turn angle counterclockwise
        for idx in (pair0, pair1):
            leftover.remove(idx)   # remove the paired edge indices


def pair_up_coords(edge1: Edge, edge2: Edge):
    """
    Pair up the coordinates of edge1 with coordinates up edge2.
    Since the directions of Edges come from walk_perimeter() and edge1 is clockwise-preceding
    edge2, adjust the directions as follows when you're adding an edge1 coordinate as key;
        - if edge1.direction is Directions.DOWN, turn it counterclockwise to Directions.RIGHT;
                                Directions.RIGHT, turn it counterclockwise to Directions.UP;
                                Directions.UP, turn it counterclockwise to Directions.LEFT;
                                Directions.LEFT, turn it counterclockwise to Directions.DOWN;
        - if edge2.direction is Directions.RIGHT, turn it clockwise to Directions.DOWN;
                                Directions.DOWN, turn it clockwise to Directions.LEFT;
                                Directions.LEFT, turn it clockwise to Directions.UP;
                                Directions.UP, turn it clockwise to Directions.RIGHT.
    When constructing the key from edge2 coordinates, reverse the counter-clockwise-turned
    edge1.direction and the clockwise-turned edge2.direction.
    """
    direction1, direction2 = turn(edge1.direction, False), turn(edge2.direction)
    for coord1, coord2 in zip(edge1.coords, reversed(edge2.coords)):
        yield (coord1, direction1), (coord2, direction2)
        yield (coord2, reverse(direction2)), (coord1, reverse(direction1))


def construct_cubewrap(grid: Grid) -> CubeWrap:
    cube_sides = identify_cube_sides(grid)
    return {
        k: v
        for edge1, edge2 in pair_up_edges(cube_sides)
        for k, v in pair_up_coords(edge1, edge2)
    }


def parse(txt_filename: str) -> tuple[Grid, Commands]:
    """
    Return the content of the file as Grid and Commands
    """
    *lines, _, line = pathlib.Path(txt_filename).read_text().splitlines()
    commands = tuple(
        str(x) if x in ('L', 'R') else int(x)
        for x in re.findall(r'L|R|\d+', line)
    )
    return Grid(lines, skip=(OFF_THE_MAP,), directions=list(Directions)), commands


def solve_part1(*puzzle_inputs) -> int:
    return compute_final_password(*follow_commands(*puzzle_inputs))


def solve_part2(*puzzle_inputs) -> int:
    return compute_final_password(*follow_commands(*puzzle_inputs, on_cube=True))


if __name__ == '__main__':
    title = 'Day 22: Monkey Map'
    print(title.center(50, '-'))

    # test that turn() works
    assert turn(Directions.RIGHT) == Directions.DOWN
    assert turn(Directions.DOWN, False) == Directions.RIGHT
    assert turn(Directions.DOWN) == Directions.LEFT 
    assert turn(Directions.LEFT, False) == Directions.DOWN
    assert turn(Directions.LEFT) == Directions.UP
    assert turn(Directions.UP, False) == Directions.LEFT
    assert turn(turn(turn(turn(Directions.UP)))) == Directions.UP

    # test that wrap_around_board() works
    boards, _ = parse('day22_test.txt')
    A, B, C, D = (6, 11), (6, 0), (7, 5), (4, 5)
    assert wrap_around_board(A, Directions.RIGHT, boards) == B
    assert wrap_around_board(C, Directions.DOWN, boards) == D
    assert wrap_around_board(B, Directions.LEFT, boards) == A
    assert wrap_around_board(D, Directions.UP, boards) == C

    # test that compute_final_password() works
    assert compute_final_password((5, 7), Directions.RIGHT) == 6032

    # test that jump_forward_left() works
    assert jump_forward_left((7, 11), Directions.DOWN) == ((8, 12), Directions.RIGHT)
    assert jump_forward_left((8, 8), Directions.UP) == ((7, 7), Directions.LEFT)
    assert jump_forward_left((7, 7), Directions.RIGHT) == ((6, 8), Directions.UP)

    # test that edges are identified
    sides = identify_cube_sides(boards)
    assert len(collections.Counter(sides)) == 14

    # test that clockwise concave intersections are identified
    clockwise_perimeter_walk_angles = [side.direction for side in sides]
    assert intersect_concave(2, 3, clockwise_perimeter_walk_angles) is True
    assert intersect_concave(0, 1, clockwise_perimeter_walk_angles) is False
    assert intersect_concave(7, 8, clockwise_perimeter_walk_angles) is True

    # test that edges have been paired if they meet at concave angles
    pairs = list(pair_up_edges(identify_cube_sides(boards)))
    assert len(collections.Counter(pairs)) == 7

    # test that the cube has been folded correctly
    test_cube: CubeWrap = {
        k: v
        for edge1, edge2 in pair_up_edges(identify_cube_sides(boards))
        for k, v in pair_up_coords(edge1, edge2)
    }
    A, B, C, D = ((5, 11), Directions.RIGHT), ((8, 14), Directions.DOWN), \
                 ((11, 10), Directions.DOWN), ((7, 1), Directions.UP)
    assert test_cube[A] == B and test_cube[(B[0], reverse(B[1]))] == (A[0], reverse(A[1]))
    assert test_cube[C] == D and test_cube[(D[0], reverse(D[1]))] == (C[0], reverse(C[1]))

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(*data)
        part2 = solve_part2(*data)
        print(f"""{file}:
        Part 1: The final password is {part1}.
        Part 2: The final password when the map is folded into a cube is {part2}.
        """)