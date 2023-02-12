"""
-- Day 22: Monkey Map --

Inspired by
    - (uses complex number)
    https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j17k7nn/?utm_source=share&utm_medium=web2x&context=3

    - (represent facing direction as a mod 4 integer)
    https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j17m65b/?utm_source=share&utm_medium=web2x&context=3

    - (folding up a cube net)
    https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j1b0fp7/?utm_source=share&utm_medium=web2x&context=3


"""
from typing import Iterator
import enum
import collections
import itertools
import operator
import re


class Direction(enum.IntFlag):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


class Tile(str, enum.Enum):
    OPEN = '.'
    WALL = '#'
    OFF = ' '


Grid: list[Tile] = []
Commands: str = ''


def parse(filename: str) -> tuple[Grid, Commands]:
    """
    Day 22's input file consists of lines of strings, a line break, and a line.
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    commands = lines.pop()  # the last line is the sequence of commands
    lines.pop() # because it's a line break
    max_length = max(len(line) for line in lines)
    grid = [
        list(map(Tile, line.ljust(max_length, ' ')))
        for line in lines
    ]
    return grid, commands


def compute_password(position: complex, facing: Direction) -> int:
    """
    Compute the final password as instructed on the prompt.
    The rows and columns are supposed to count from 1 instead of python
    default 0, so increment them by 1.
    """
    return 1000 * (int(position.real) + 1) +\
        4 * (int(position.imag) + 1) +\
        [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP].index(facing)


Grid, Commands = parse('day22_test.txt')
Start = 0 + Grid[0].index(Tile.OPEN) * 1j
position, facing = Start, Direction.RIGHT

WrapTo = collections.defaultdict(lambda: collections.defaultdict(int))


# part 1
def construct_board_wrap(grid: Grid) -> dict:
    """
    Construct a dictionary that shows which row or column index
    to jump to if you're on some column or row facing some direction.
    """
    for n, line in enumerate(grid):
        left_edge: int = next(
            filter(
                lambda j: line[j] != Tile.OFF,
                range(len(line))
            )
        )
        right_edge: int = next(
            filter(
                lambda j: line[j] != Tile.OFF,
                range(len(line)-1, -1, -1)
            )
        )
        if Grid[n][left_edge] == Tile.OPEN:
            WrapTo[Direction.RIGHT][n] = left_edge
        if Grid[n][right_edge] == Tile.OPEN:
            WrapTo[Direction.LEFT][n] = right_edge

    grid_t = list(zip(*grid))
    for m, vertical_line in enumerate(grid_t):
        top_edge = next(
            filter(
                lambda j: vertical_line[j] in '.#',
                range(len(vertical_line))
            )
        )
        bottom_edge = next(
            filter(
                lambda j: vertical_line[j] in '.#',
                range(len(vertical_line)-1, -1, -1)
            )
        )
        if Grid[bottom_edge][m] == Tile.OPEN:
            WrapTo[Direction.UP][m] = bottom_edge
        if Grid[top_edge][m] == Tile.OPEN:
            WrapTo[Direction.DOWN][m] = top_edge

    return WrapTo


WrapTo = construct_board_wrap(Grid)


def wrap(position: complex, facing: Direction) -> complex:
    match facing:
        case Direction.RIGHT:
            return position.real + WrapTo[facing][position.real] * 1j
        case Direction.LEFT:
            return position.real + WrapTo[facing][position.real] * 1j
        case Direction.UP:
            return WrapTo[facing][position.imag] + position.imag * 1j
        case Direction.DOWN:
            return WrapTo[facing][position.imag] + position.imag * 1j


for move in re.findall(r'\d+|[RL]', Commands):
    match move:
        case 'R':
            facing = Direction((facing - 1) % 4)
        case 'L':
            facing = Direction((facing + 1) % 4)
        case _:
            for _ in range(int(move)):
                new_position = position + (1j**facing)
                row, column = int(new_position.real), int(new_position.imag)
                if len(Grid) <= row\
                        or len(Grid[0]) <= column\
                        or Grid[row][column] == Tile.OFF:
                    new_position = wrap(new_position, facing)
                    row, column = int(new_position.real), int(new_position.imag)
                if Grid[row][column] == Tile.OPEN:
                    position = new_position

print(f'Part 1: {compute_password(position, facing)}')  # 20494


# part 2

Edge = collections.namedtuple('Edge', ['direction', 'positions'])


def walk_perimeter_wo_inner_corner() -> Iterator[Edge]:
    """
    Walk around the perimeter except for the inner corners
    (e.g. 8 + 11j on the test input grid is skipped over because it's an inner corner).
    """

    def jump_left_front(position: complex, dir: Direction):
        """ Do a chess knight move """
        match dir:
            case Direction.RIGHT:
                return position + (-1 + 1j)
            case Direction.DOWN:
                return position + (1 + 1j)
            case Direction.LEFT:
                return position + (1 - 1j)
            case Direction.UP:
                return position + (-1 - 1j)

    pos, dir = Start, Direction.RIGHT
    edge = collections.deque()
    looped = False
    while not looped:
        edge.append(pos)
        step_forward = pos + (1j ** dir)
        i, j = int(step_forward.real), int(step_forward.imag)
        if not (0 <= i < len(Grid)) \
                or not (0 <= j < len(Grid[0])) \
                or Grid[i][j] == Tile.OFF:
            yield Edge(dir, tuple(edge))
            edge.clear()
            dir = Direction((dir - 1) % 4)
        else:
            left_front = jump_left_front(pos, dir)
            i, j = int(left_front.real), int(left_front.imag)
            if not (0 <= i < len(Grid)) \
                    or not (0 <= j < len(Grid[0])) \
                    or Grid[i][j] == Tile.OFF:
                pos = step_forward
            else:
                yield Edge(dir, tuple(edge))
                edge.clear()
                dir = Direction((dir+1) % 4)
                pos = left_front
        looped = (pos == Start) and (dir == Direction.RIGHT)


def group_into_edges() -> list[Edge]:
    """
    Break each item returned by walk_perimeter_wo_inner_corner() into equal length edges.
    """
    side = min(
        sum(
            map(lambda pt: pt != Tile.OFF, line)
        )
        for line in Grid
    )
    return [
        Edge(direction=dir, positions=points[start: start + side])
        for dir, points in walk_perimeter_wo_inner_corner()
        for start in range(0, len(points), side)
    ]


def pair_up_edges(edges: list[Edge]) -> Iterator[tuple[Edge, Edge]]:
    """
    Pair up edges if they form a concave intersection, which is
    detected when the mod 4 difference of the second edge's Direction and
    the first edge's Direction equals 1.
    """
    while edges:
        i = 0
        while i < len(edges) - 1:
            edge1, edge2 = edges[i], edges[i + 1]
            if (edge2.direction - edge1.direction) % 4 == 1:
                yield (edge1, edge2)
                edges[i: i + 2] = []
                edges[i:] = map(
                        lambda edge:
                            edge._replace(
                                direction=Direction((edge.direction + 1) % 4)
                            ),
                        edges[i:]
                    )
            else:
                i += 1


edges = group_into_edges()
paired = pair_up_edges(edges)
CubeWrapTo = {}
for edge1, edge2 in paired:
    dir1, dir2 = edge1.direction, edge2.direction
    print(edge1)
    print(edge2)



