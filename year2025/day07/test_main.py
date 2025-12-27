import pytest

import main as solution

@pytest.fixture
def example() -> solution.Grid:
    return solution.parse('example.txt')

def test_parse(example):
    assert next(example.find_cells('S')) == (0, 7)
    splitters = set(example.find_cells('^'))
    assert (2, 7) in splitters
    assert (8, 4) in splitters
    assert len(splitters) == 22
    assert not example[(16, 10)]

def test_will_split_beam(example):
    assert solution.will_split_beam((2, 7), example)
    assert solution.will_split_beam((4, 6), example)
    assert solution.will_split_beam((8, 6), example)

def test_will_not_split_beam(example):
    assert not solution.will_split_beam((14, 9), example)

def test_solve_part1(example):
    assert solution.solve_part1(example) == 21

def test_propogate(example):
    start = next(example.find_cells('S'))
    timelines = {start[solution.COLUMN] : 1}

    assert solution.propogate(timelines, {}) == {7: 1}
    assert solution.propogate(timelines, {7}) == {6:1, 8:1}

def test_solve_part2(example):
    assert solution.solve_part2(example) == 40