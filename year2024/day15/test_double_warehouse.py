#test_double_warehouse.py
from textwrap import dedent
from contextlib import nullcontext

import pytest

from main import DoubleWarehouse, OBOX, LBOX, RBOX
from Grid import NORTH, SOUTH, WEST, EAST

GRID = dedent(
    """\
    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######
    """
)
S0 = DGRID = dedent(
    """\
    ##############
    ##......##..##
    ##..........##
    ##....[][]@.##
    ##....[]....##
    ##..........##
    ##############
    """
)
S1 = dedent(
    """\
    ##############
    ##......##..##
    ##..........##
    ##...[][]@..##
    ##....[]....##
    ##..........##
    ##############
    """
)
A0 = dedent(
    """\
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##############
    """
)
A1 = dedent(
    """\
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##..........##
    ##############
    """
)
TEST_GPS1 = dedent(
    """\
    ##########
    ##...[]...
    ##........
    """
)
TEST_GPS2 = dedent(
    """\
    ####################
    ##[].......[].[][]##
    ##[]...........[].##
    ##[]........[][][]##
    ##[]......[]....[]##
    ##..##......[]....##
    ##..[]............##
    ##..@......[].[][]##
    ##......[][]..[]..##
    ####################
    """
)


def test_double_warehouse():
    assert DoubleWarehouse.double(GRID) ==\
        DoubleWarehouse(DGRID)
    assert not DoubleWarehouse(DGRID).find_cells(OBOX)


@pytest.fixture
def setup():
    return DoubleWarehouse(DGRID)


@pytest.mark.parametrize(
    'here, expected',
    [
        ((3, 6), True),
        ((3, 7), True),
        ((1, 7), False)
    ]
)
def test_has_movable_item(setup, here, expected):
    assert setup.has_movable_item(here) == expected


@pytest.mark.parametrize(
    'data, direction, expected',
    [
        (S0, NORTH, {(3, 10)}),
        (S0, WEST, {(3, 10), (3, 9), (3, 8), (3, 7), (3, 6)}),
        (
            A0, NORTH, 
            {(3, 5), (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (5, 7)}
        ),
        (
            A1, NORTH,
            {(2, 5), (2, 6), (2, 7), (2, 8), (3, 6), (3, 7), (4, 7)}
        )
    ]
)
def test_get_movable_items(data, direction, expected):
   warehouse = DoubleWarehouse(data)
   actual = warehouse.get_movable_items(direction)
   assert actual == expected


@pytest.mark.parametrize(
    'data, direction, expected',
    [
        (S0, WEST, S1),
        (A0, NORTH, A1),
        (A1, NORTH, A1)
    ]
)
def test_shift_items(data, direction, expected):
    warehouse = DoubleWarehouse(data)
    warehouse.shift_items(direction)
    assert warehouse == DoubleWarehouse(expected)


@pytest.mark.parametrize(
    'data, expected',
    [(TEST_GPS1, 105), (TEST_GPS2, 9021)]
)
def test_get_total_gps(data, expected):
    warehouse = DoubleWarehouse(data)
    assert warehouse.get_total_gps() == expected