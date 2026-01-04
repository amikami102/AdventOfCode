from pathlib import Path
from typing import Iterable, Iterator

import pytest

import main as solution


@pytest.fixture
def example() -> Iterable[solution.Coordinate]:
    return solution.parse('example.txt')


def test_area():
    assert solution.calculate_area((2, 5), (9, 7)) == 24
    assert solution.calculate_area((7, 1), (11, 7)) == 35
    assert solution.calculate_area((7, 3), (2, 3)) == 6
    assert solution.calculate_area((2, 5), (11, 1)) == 50


def test_solve_part1(example):
    assert solution.solve_part1(example) == 50


def test_solve_part2(example):
    assert solution.solve_part2(example) == 24