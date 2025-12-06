# year2025/day02/test_main.py
from typing import Iterable
import pytest

import main as solution

@pytest.fixture
def example() -> Iterable[str]:
    return solution.parse('example.txt')

def test_parse_range(example):
    lines = [
        solution.parse_range(line)
        for line in example
    ]
    assert lines[0] == range(11, 23)
    assert lines[4] == range(222220, 222225)
    assert lines[7] == range(38593856, 38593863)

@pytest.mark.parametrize(
    'product_id, expected',
    [
        ('22', True), 
        ('6464', True),
        ('6465', False),
        ('1188511885', True),
        ('1698522', False)
    ]
)
def test_sequence_repeated_twice(product_id, expected):
    assert solution.sequence_repeated_twice(product_id) == expected

@pytest.mark.parametrize(
    'product_id, expected',
    [
        ('22', True), 
        ('6464', True),
        ('1188511885', True),
        ('565656', True),
        ('999', True),
    ]
)
def test_sequence_repeated_twice_or_more(product_id, expected):
    assert solution.sequence_repeated_twice_or_more(product_id) == expected

def test_on_example(example):
    assert solution.solve_part1(example) == 1227775554
    assert solution.solve_part2(example) == 4174379265