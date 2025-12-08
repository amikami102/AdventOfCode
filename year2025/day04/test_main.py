from pathlib import Path
from typing import Iterable
from dataclasses import dataclass

import pytest

import main as solution


example_solution = """\
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x."""

@dataclass
class Example:
    problem = solution.Grid(
        solution.parse('example.txt'),
        directions=solution.EIGHT)
    solution = solution.Grid(
        example_solution.splitlines(),
        directions=solution.EIGHT)

@pytest.fixture
def example() -> Example:
    return Example()

def test_count_rolls_nearby(example):
    assert solution.count_rolls_nearby(
        example.problem, (3, 4)) == 7
    assert solution.count_rolls_nearby(
        example.problem, (1, 0)) == 3

def test_solve_part1():
    data = solution.parse('example.txt')
    assert solution.solve_part1(data) == 13

def test_solve_part2():
    data = solution.parse('example.txt')
    assert solution.solve_part2(data) == 43