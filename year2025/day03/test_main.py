from pathlib import Path
from typing import Iterable

import pytest

import main as solution


@pytest.fixture
def example() -> Iterable[str]:
    return Path('example.txt').read_text().splitlines()

@pytest.mark.parametrize(
    'batteries,k,expected',
    [
        ([9,8,7,6,5,4,3,2,1,1,1,1,1,1,1], 2, 98),
        ([8,1,1,1,1,1,1,1,1,1,1,1,1,1,9], 2, 89),
        ([2,3,4,2,3,4,2,3,4,2,3,4,2,7,8], 2, 78),
        ([8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], 2, 92),
        ([9,8,7,6,5,4,3,2,1,1,1,1,1,1,1], 12, 987654321111),
        ([8,1,1,1,1,1,1,1,1,1,1,1,1,1,9], 12, 811111111119),
        ([2,3,4,2,3,4,2,3,4,2,3,4,2,7,8], 12, 434234234278),
    ]
)
def test_select_largest_joltage(batteries, k, expected):
    assert sum(solution.select_largest_joltage(batteries, k)) == expected

def test_on_example(example):
    assert solution.solve_part1(example) == 357
    assert solution.solve_part2(example) == 3121910778619