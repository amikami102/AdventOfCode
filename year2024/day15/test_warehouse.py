# test_warehouse_class.py
from textwrap import dedent
from contextlib import nullcontext

import pytest

from main import Warehouse
from Grid import EAST, WEST


GRID = dedent(
    """\
    #########
    #@O.O.OO#
    #########
    """
)
INVALID_GRID = dedent(
    """\
    #########
    #@@@@@@@#
    #########
    """
)
TEST_GPS = dedent(
    """\
    #######
    #...O..
    #......
    """
)
GRID1 = dedent(
    """\
    #########
    #.@OO.OO#
    #########
    """
)
GRID2 = dedent(
    """\
    #########
    #..@OOOO#
    #########
    """
)


@pytest.fixture
def warehouse():
    return Warehouse(GRID)


@pytest.mark.parametrize(
    'data, expectation',
    [
        (GRID, nullcontext()),
        (INVALID_GRID, pytest.raises(ValueError))
    ]
)
def test_locate_robot(data, expectation):
    warehouse = Warehouse(data)
    with expectation:
        bots = warehouse.locate_robot()
        assert len([bots]) == 1


@pytest.mark.parametrize(
    'start, direction, expected',
    [
        ((1, 1), EAST, [(1, i) for i in range(1, 3)]),
        ((1, 1), WEST, [(1, 1)])
    ]
)
def test_get_movable_items(warehouse, start, direction, expected):
    actual = warehouse.get_movable_items(direction, start)
    assert list(actual) == expected


@pytest.mark.parametrize(
    'data, direction, expected',
    [
        (GRID, EAST, GRID1),
        (GRID, WEST, GRID),
        (GRID1, EAST, GRID2)
    ]
)
def test_shift_items(data, direction, expected):
    setup = Warehouse(data)
    setup.shift_items(direction)
    assert setup == Warehouse(expected)

@pytest.mark.parametrize(
    'data, expected',
    [(TEST_GPS, 104), (GRID2, 104 + 105 + 106 + 107)]
)
def test_get_total_gps(data, expected):
    actual = Warehouse(data).get_total_gps() 
    assert actual == expected
