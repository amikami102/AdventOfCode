from operator import add, mul
from typing import Iterable

import pytest

import main as solution

@pytest.fixture
def example() -> Iterable[str]:
    return solution.parse('example.txt')


def test_get_operator():
    assert solution.get_operator('+') == add
    assert solution.get_operator('*') == mul
    with pytest.RaisesExc(ValueError):
        solution.get_operator('-')

@pytest.mark.parametrize(
    'numbers,symbol,expected',
    [
        (('1', '2', '3'), '+', 6),
        (('10', '2', '3'), '*', 60)
    ]
)
def test_solve(numbers, symbol, expected):
    assert solution.solve(*numbers, symbol=symbol)==expected


def test_organize_by_columns(example):
    assert list(solution.organize_by_columns(example))\
    == [
        ('123', '45', '6', '*'), 
        ('328', '64', '98', '+'), 
        ('51', '387', '215', '*'), 
        ('64', '23', '314', '+')
    ]
    assert list(solution.organize_by_columns(example, True))\
        == [
            ('356', '24 ', '1  ', '*'), 
            ('8  ', '248', '369', '+'), 
            ('175', '581', ' 32', '*'),
            ('  4', '431', '623', '+')
        ]

def test_solve_part1(example):
    assert solution.solve_part1(example) == 4277556

def test_solve_part2(example):
    assert solution.solve_part2(example) == 3263827