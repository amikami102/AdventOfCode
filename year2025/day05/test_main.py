from typing import Iterable, Generator

import pytest

import main as solution
from main import rangeComponent

def list_rangeComponents(
        pairs: Iterable[tuple[int,int]]
        ) -> list[rangeComponent]:
    return [
        rangeComponent(*pair)
        for pair in pairs
    ]

@pytest.fixture
def example() -> tuple[list[str], list[str]]:
    fresh_ranges, available_ingredients = \
        solution.parse('example.txt')
    return fresh_ranges, available_ingredients

@pytest.mark.parametrize(
    'input,expected',
    [
        ('1-2', [(1,1), (2,-1)]),
        ('10-100', [(10,1), (100,-1)])
    ]
)
def test_parse_ranges(input, expected):
    assert list(solution.parse_range_line(input)) == \
        list_rangeComponents(expected)

@pytest.mark.parametrize(
    'input,expected',
    [
        (
            [(1,1), (2,-1), (10,1), (100,-1)], 
            [(1,1), (2,-1), (10,1), (100,-1)]
        ),
        (
            [(1,1), (5,-1), (2,1), (6,-1)],
            [(1,1), (2,1), (5,-1), (6,-1)]
        ),
        (
            [(1,1), (5,-1), (1,1), (3,-1)],
            [(1,1), (1,1), (3,-1), (5,-1)] 
        ),
        (
            [(1,1), (5,-1), (-2,1), (1,-1)],
            [(-2,1), (1,1), (1,-1), (5,-1)] 
        )
    ]
)
def test_sort_components(input, expected):
    input_components = iter(list_rangeComponents(input))
    assert list(solution.sort_components(input_components))\
        == list_rangeComponents(expected)


@pytest.mark.parametrize(
    'input,expected',
    [
        (
            [(1,1), (2,-1), (10,1), (100,-1)],
            [(1,2),(10,100)]
        ),
        (
            [(1,1), (2,1), (5,-1), (6,-1)],
            [(1,6)]
        ),
        (
            [(1,1), (1,1), (3,-1), (5,-1)],
            [(1,5)]
        ),
        (
            [(-2,1), (1,1), (1,-1), (5,-1)],
            [(-2,5)]
        )
    ]
)
def test_merge_ranges(input, expected):
    input_components = iter(list_rangeComponents(input))
    assert list(solution.merge_ranges(input_components)) == expected

def test_solve_part1(example):
    assert solution.solve_part1(example) == 3

def test_solve_part2(example):
    assert solution.solve_part2(example) == 14