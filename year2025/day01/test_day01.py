from typing import Iterable
from pathlib import Path

import pytest
import main as solution

@pytest.fixture
def example() -> Iterable[str]:
    return solution.parse('test.txt')

def test_parse():
    assert list(example()) == [
        'L68',
        'L30',
        'R48',
        'L5',
        'R60',
        'L55',
        'L1',
        'L99',
        'R14',
        'L82']
    
def test_parse_rotation():
    assert solution.parse_rotation('L30') == ('L', 30)
    assert solution.parse_rotation('R99') == ('R', 99)
    assert solution.parse_rotation('R0') == ('R', 0)
    with pytest.raises(ValueError):
        solution.parse_rotation('R')

@pytest.mark.parametrize(
    "inputs, result",
    [
        ([11, 'r', 8], 19),
        ([5, 'l', 10], 95),
        ([95, 'l', 95], 0),
        ([0, 'l', 1], 99),
        ([99, 'r', 1], 0),
        ([55, 'l', 155], 0),
        ([50, 'r', 1000], 50)
    ]
)
def test_turn(inputs, result):
    assert solution.turn(*inputs) == result

@pytest.mark.parametrize(
    "current, rotation, result",
    [
        (0, 'R200', 2),     # passes through 0 once and lands on 0
        (99, 'R200', 2),
        (50, 'R1000', 10),  # passes through 0 nine times before returning to 0
        (50, 'R68', 1),
        (50, 'R50', 1),
        (99, 'L99', 1),
        (95, 'R60', 1),
        (55, 'L155', 2),    # passes through 0 once and lands on 0
        (0, 'L5', 0),
        (1, 'L5', 1),
        (0, 'L1', 0),
        (0, 'L99', 0),      # lands on 1 and does not pass through 0
        (0, 'L100', 1),     # lands on 0
        (99, 'L99', 1),     # lands on 0
        (99, 'L100', 1),    # passes through 0 to return to 99
        (50, 'L48', 0),
        (2, 'L3', 1),       # passes through 0 once before landing on 99
        (2, 'L103', 1),     # passes through 0 twice before landing on 99
        (99, 'R6', 1),
        (50, 'R50',1),
        (0, 'L1', 0),
        (0, 'L50', 0)
    ]
)
def test_count_passes_through_zero(current, rotation, result):
    assert solution.count_passes_through_zero(
            current, 
            *solution.parse_rotation(rotation)
        ) == result

def test_solve_part1(example):
    assert solution.solve_part1(example) == 3
    
def test_solve_part2(example):
    assert solution.solve_part2(example) == 6