"""
-- Day 09: Rope Bridge --

Usage example:
    Advent_Of_Code/year2022 $ python day09_rope_bridge.py day09_test.txt day09_input.txt
"""
import sys
import pathlib
import itertools
import collections
from typing import *

T = TypeVar('T')
Coord = tuple[int, int]     # (row, column)
Vector = Coord
Command = tuple[str, int]

ROW, COLUMN = 0, 1
ZERO: Coord = (0, 0)
DIRECTIONS = Right, Left, Up, Down = (0, 1), (0, -1), (-1, 0), (1, 0)
LOOKUP: dict[str, Vector] = {
    'R': Right,
    'L': Left,
    'U': Up,
    'D': Down
}


def parse(txt_filename: str) -> list[Command]:
    return [
        (
            line.split(' ')[0],
            int(line.split(' ')[1])
        )
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[ROW] + vector2[ROW], vector1[COLUMN] + vector2[COLUMN]


def _write_head_history(commands: Iterable[Command]) -> list[Coord]:
    """Write the history of Head knot"""
    history = [ZERO]
    for move in commands:
        direction, n = move
        history.extend([LOOKUP[direction]] * n)
    return list(itertools.accumulate(history, _add_vectors))


def _update_tail_coord(tail: Coord, head: Coord) -> Coord:
    """
    Return the vector the tail needs to move so that the tail is touching the head.
    """
    drow, dcol = (head[ROW] - tail[ROW]), (head[COLUMN] - tail[COLUMN])
    if abs(drow) <= 1 and abs(dcol) <= 1:
        return tail
    elif abs(drow) > 1 or abs(dcol) > 1:
        return _add_vectors(
            tail,
            (
                1 * int(drow/abs(drow)) if drow != 0 else 0,
                1 * int(dcol/abs(dcol)) if dcol != 0 else 0
            )
        )


def solve_part1(puzzle_input: list[Command]) -> int:
    """
    Count the number of coordinates the tail visits as its coordinate is updated by the head's movement.
    """
    head_history = _write_head_history(puzzle_input)
    tail_history = [ZERO]
    for coord in head_history:
        tail_history.append(_update_tail_coord(tail_history[-1], coord))
    return len(set(tail_history))


def solve_part2(puzzle_input: list[Command]) -> int:
    """
    Same as part 1, but now there are nine tail knots.
    Count the number of coordinates visited by the 9th tail knot.
    """
    head_history = _write_head_history(puzzle_input)
    knots = (head_history, *([ZERO] for _ in range(9)))
    for (header_history, tailer_history) in itertools.pairwise(knots):
        for coord in header_history:
            tailer_history.append(
                _update_tail_coord(tailer_history[-1], coord)
            )
    return len(set(knots[-1]))


if __name__ == '__main__':
    title = 'Day 09: Rope Bridge'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The tail visits {part1} different locations at least once.
        Part 2: The ninth tail visits {part2} different locations at least once.
        """)
