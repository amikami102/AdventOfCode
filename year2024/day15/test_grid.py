# test_grid_class.py
from textwrap import dedent
from contextlib import nullcontext
import pytest

from Grid import * 


DATA: str = dedent(
    """\
    e...a
    .d.b.
    ..c..
    .d.b.
    e...a
    """
)
SW = add_coordinates(SOUTH, WEST)


@pytest.fixture
def simple_grid():
    grid = Grid(DATA.splitlines())
    return grid 


@pytest.mark.parametrize(
    'data, skip, expected', 
    [(DATA, [], 25), (DATA, {'.'}, 9)]
)
def test_skip_kwarg(data, skip, expected):
    grid = Grid(data.splitlines(), skip=skip)
    assert len(grid) == expected


@pytest.mark.parametrize(
    'data, default, testkey, expectation',
    [
        (DATA, KeyError, (0, 5), pytest.raises(KeyError)),
        (DATA, None, (0, 5), nullcontext())
    ]
)
def test_default_kwarg(data, default, testkey, expectation):
    grid = Grid(data.splitlines(), default=default)
    with expectation:
        assert grid[testkey] is None


@pytest.mark.parametrize('target, expected', [
    ('a', [(0, 4), (4, 4)]),
    ('c', [(2, 2)]),
    ('f', []),
])
def test_find_cells(simple_grid, target, expected):
    assert simple_grid.find_cells(target) == expected


@pytest.mark.parametrize(
    'start, direction, expected',
    [
        ((0, 0), SOUTH, [(i, 0) for i in range(5)]),
        ((2, 2), EAST, [(2, i) for i in range(2, 5)]),
        ((0, 4), SW, [(i, 4-i) for i in range(0, 5)])
    ]
)
def test_down_the_line(simple_grid, start, direction, expected):
    actual = list(simple_grid.down_the_line(start, direction)) 
    assert actual == expected


def test_convert_to_list_of_rows(simple_grid):
    actual = simple_grid.convert_to_list_of_rows()
    expected = [list(line) for line in DATA.splitlines()]
    assert actual == expected
