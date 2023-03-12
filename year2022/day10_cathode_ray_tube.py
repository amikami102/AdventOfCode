"""
-- Day 10: Cathode Ray Tube --

Usage example:
    Advent_Of_Code/year2022 $ python day10_cathode_ray_tube.py day10_test.txt day10_input.txt
"""
import sys
import pathlib
import functools
import itertools
from typing import *

SCREEN_WIDTH: int = 40
LIT, DARK = '#', '.'
ADDX = 'addx'


def parse(txt_filename: str) -> list[list[str]]:
    separator = functools.partial(str.split, sep=' ')
    return list(
            map(separator, pathlib.Path(txt_filename).read_text().splitlines())
        )


def _execute_program(commands: list[list[str]]) -> Iterator[int]:
    """
    Yield the register of X during the cycle,
    i.e. when X is updated at the end of the cycle by addx command,
    the updated X appears in the next iteration.
    """
    X: int = 1
    yield X
    for command in commands:
        op, *args = command
        if op == ADDX:
            yield X
            X += int(args[0])
        yield X


def solve_part1(puzzle_input: list[list[str]]) -> int:
    """
    Execute the program by feeding the puzzle input to _execute_program.
    Add the X register during the cycle multiplied by the cycle number for
    cycles in `range(20, 220+1, 40)`.
    Cycles start counting from 1.
    """
    return sum(
        i * cycle for i, cycle in enumerate(_execute_program(puzzle_input), start=1)
        if i in range(20, 220 + 1, 40)
    )


def _draw_pixel(position: int, X: int) -> str:
    """
    Return LIT if mod(position, SCREEN_WIDTH) is in (X-1, X, X+1), otherwise DARK.
    """
    return LIT if position % SCREEN_WIDTH in (X-1, X, X+1) else DARK


def solve_part2(puzzle_input: list[list[str]]) -> str:
    """
    Like part1, feed the puzzle_input into _execute_program().
    Draw pixels according to the cycle number and the X register during the cycle.
    Format the pixels to fit in the screen width.
    """
    pixels = [
        _draw_pixel(i, X)
        for i, X in enumerate(_execute_program(puzzle_input))
    ]
    lines = [iter(pixels)] * SCREEN_WIDTH
    return '\n'.join(
        ''.join(itertools.chain(*line))
        for line in zip(*lines)
    )


if __name__ == '__main__':
    title = 'Day 10: Cathode Ray Tube'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The total strength of the six cycles is {part1}.
        Part 2: The letters displayed on the screen are\n{part2}.
        """)
