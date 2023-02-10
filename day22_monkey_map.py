"""
-- Day 22: Monkey Map --

Inspired by
    - (uses complex number)
    https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j17k7nn/?utm_source=share&utm_medium=web2x&context=3

    - (represent facing direction as a mod 4 integer)
    https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j17m65b/?utm_source=share&utm_medium=web2x&context=3

    - (programmatically determine the board wrap)
    https://github.com/taylorott/Advent_of_Code/blob/94c084b2ca1b1f9df34eebf7c561822d4bd84f9c/src/Year_2022/Day22/Solution.py

"""
import enum
import collections
import re


class Direction(enum.IntFlag):
    RIGHT = 1
    LEFT = 3
    UP = 2
    DOWN = 0


class Tile(str, enum.Enum):
    OPEN = '.'
    WALL = '#'
    OFF = ' '


Grid: list[Tile] = []
Commands: str = ''
Position: complex
Facing: Direction


def parse(filename: str) -> tuple[Grid, Commands]:
    """
    Day 22's input file consists of lines of strings, a line break, and a line.
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    commands = lines.pop()
    lines.pop()
    max_length = max(len(line) for line in lines)
    grid = [
        list(map(Tile, line.ljust(max_length, ' ')))
        for line in lines
    ]
    return grid, commands


Grid, Commands = parse('day22_input.txt')
Position, Facing = 0 + Grid[0].index(Tile.OPEN) * 1j, Direction.RIGHT
print(len(Grid), len(Grid[1]))

WrapTo = collections.defaultdict(lambda: collections.defaultdict(int))


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


def wrap(position: Position, facing: Facing) -> complex:
    match facing:
        case Direction.RIGHT:
            return position.real + WrapTo[facing][position.real] * 1j
        case Direction.LEFT:
            return position.real + WrapTo[facing][position.real] * 1j
        case Direction.UP:
            return WrapTo[facing][position.imag] + position.imag * 1j
        case Direction.DOWN:
            return WrapTo[facing][position.imag] + position.imag * 1j


def compute_password(position: Position, facing: Facing) -> int:
    """
    Compute the final password.
    """
    return 1000 * (int(position.real) + 1) +\
        4 * (int(position.imag) + 1) +\
        [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP].index(facing)


for move in re.findall(r'\d+|[RL]', Commands):
    match move:
        case 'R':
            Facing = Direction((Facing - 1) % 4)
        case 'L':
            Facing = Direction((Facing + 1) % 4)
        case _:
            for _ in range(int(move)):
                new_position = Position + (1j**Facing)
                row, column = int(new_position.real), int(new_position.imag)
                print(row, column, Position, Facing)
                if len(Grid) <= row\
                        or len(Grid[0]) <= column\
                        or Grid[row][column] == Tile.OFF:
                    new_position = wrap(new_position, Facing)
                    row, column = int(new_position.real), int(new_position.imag)
                if Grid[row][column] == Tile.OPEN:
                    Position = new_position

print(compute_password(Position, Facing))

