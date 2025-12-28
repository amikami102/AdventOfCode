from pathlib import Path
from typing import Iterable

import pytest

import main as solution

pair1 = (162,817,812), (425,690,689)
pair2 = (162,817,812), (431,825,988)
pair3 = (906,360,560), (805,96,715)
pair4 = (431,825,988), (425,690,689)

@pytest.fixture
def example() -> Iterable[solution.Junction]:
    return solution.parse('example.txt')


def test_pair_and_sort_junctions(example):
    paired_and_sorted = iter(
        solution.pair_and_sort_junctions(example))
    assert next(paired_and_sorted) == pair1
    assert next(paired_and_sorted) == pair2


def test_combine_circuits(example):
    assert {*pair1} in solution.combine_circuits(example, 1)
    assert {*pair1, *pair2} in solution.combine_circuits(example, 2)
    assert {*pair1, *pair2} in solution.combine_circuits(example, 3)
    assert {*pair3} in solution.combine_circuits(example, 3)
    assert len(solution.combine_circuits(example, 3)) == 17
    assert len(solution.combine_circuits(example, 4)) == 17


def test_solve_part1(example):
    assert solution.solve_part1(example, limit=10) == 40

def test_solve_part2(example):
    assert solution.solve_part2(example, limit=None) == 25272