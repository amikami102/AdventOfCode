"""
-- Day 17: Pyroclastic Flow --

Usage example:
    Advent_Of_Code/year2022 $ python day17_pyroclastic_flow.py day17_test.txt day17_input.txt

Inspired by this very fast solution, https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0vj0l2/?utm_source=share&utm_medium=web2x&context=3

Part 1 can be solved by simulating N=2022 rocks falling through the tower, but this method doesn't work for part 2 where N=1_000_000_000_000. The code is written to solve both parts with the same set of functions.

To solve part 2 efficiently, assume that repeating through the same sequence of jets and five rocks in the same order will create a cycle.
The parameters we need in order to compute the final height are
    - the length of the cycle (`period`);
    - the last index before the first period begins;
    - the amount the tower grows per cycle (`delta_height`).

The cycle will be determined while simulating the tetris process. During the simulation, we will keep track of the following data each simulation round:
    - the rock index (0, 1, 2, 3, or 4);
    - the jet index (0, 1, ..., J);
    - the leftmost row index where the indexed rock that has stopped moving (0, 1, 2, ..., 6);
    - the height of the tower.
"""
import sys
import pathlib
import collections
import itertools
import functools
from dataclasses import dataclass
from typing import *

Coord = tuple[int, int]  # (x, y)
Vector = Coord
Rock = set[Coord]

CHAMBER_WIDTH: int = 7
X_OFFSET, Y_OFFSET = 2, 4
X, Y = 0, 1
DIRECTIONS = Left, Right, Down = (-1, 0), (1, 0), (0, 1)
ARROWS: dict[str, Vector] = {'>': Right, '<': Left, 'v': Down}


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[X] + vector2[X], vector1[Y] + vector2[Y]


def _slide(coords: Iterable[Coord], dx: int = 0, dy: int = 0) -> set[Coord]:
    """
    Slide the coords horizontally dx units and vertically dy units.
    """
    return set(map(lambda coord: _add_vectors(coord, (dx, dy)), coords))


def _shape(*lines) -> Rock:
    """
    Extract the coordinates of '#' characters in successive lines
    depicting a rock top down.
    e.g. '.####' becomes [(0,1), (0,2), (0, 3), (0,4)]
    """
    return {
        (x, y)
        for y, line in enumerate(lines)
        for x, value in enumerate(line)
        if value == '#'
    }


ROCKS: list[Rock] = [
    _shape('####'),
    _shape('.#.', '###', '.#.'),
    _shape(
        '..#',
        '..#',
        '###'
    ),  # note that the lines are listed top down
    _shape('#', '#', '#', '#'),
    _shape('##', '##')
]
FLOOR = _shape('#' * CHAMBER_WIDTH)


class Tower(set):
    def __init__(self):
        super().__init__(set() | FLOOR)

    def rock_appears(self, rock: Rock) -> Rock:
        """
        Place the bottom of the rock at the top of the tower when it first appears.
        1. Slide the rock up `min(layer[Y] for layer in tower)` units
            so that the top of the rock (the coordinates with y = 0) is at the top of the tower.
        3. Slide the rock up `max(layer[Y] for layer in rock)` units
            so that the bottom of the rock is sitting at the top of the tower.
        4. Slide up so that there are 3 units between the top of the tower and the bottom of the rock.
        """
        dy = min(layer[Y] for layer in self) \
            - max(layer[Y] for layer in rock) \
            - Y_OFFSET
        return _slide(rock, X_OFFSET, dy)

    def move_rock(self, rock: Rock, arrow: str) -> Rock:
        """
        Move the rock in the direction specified by `arrow`.
        Return the original rock if the rock hits the wall or hits any coordinate in `tower`; otherwise, return the moved rock.
        """
        rock_if = _slide(rock, *ARROWS[arrow])
        return rock if any(
                coord[X] not in range(CHAMBER_WIDTH)
                or coord in self
                for coord in rock_if
            ) else rock_if


def _simulate(rock_idx: int, rock: Rock, tower: Tower, jets: Iterator[tuple[int, str]]) -> tuple[int, ...]:
    """
    Simulate the rock falling through the tower until it stops.
    """
    rock0 = tower.rock_appears(rock)
    x_left = X_OFFSET
    while True:
        jet_idx, jet = next(jets)
        rock1 = tower.move_rock(rock0, jet)
        rock0 = tower.move_rock(rock1, 'v')
        if rock0 == rock1:
            # the rock couldn't move down after being jetted
            tower |= rock0
            break
        else:
            # update the leftmost index of the rock
            x_left = min(point[X] for point in rock0)
    height = abs(min(layer[Y] for layer in tower))
    return rock_idx, jet_idx, x_left, height


@dataclass
class PeriodicSequence:
    period: int = 0
    heights: list[int] = 0
    index_before_first_period: int = 0

    def compute_final_height(self, n_rocks: int) -> int:
        """
        Compute the final height of the tower after n_rocks have been dropped down the tower.
        """
        # determine how many periods there are in n_rocks
        n_periods, remainder = divmod(n_rocks - self.index_before_first_period, self.period)
        # determine the amount of growth per period
        delta_height = self.heights[self.index_before_first_period + self.period] - \
            self.heights[self.index_before_first_period]
        return self.heights[self.index_before_first_period + remainder - 1] + \
            delta_height * n_periods


def _determine_period(jets: str, max_rocks: int = 2022) -> PeriodicSequence | None:
    out = PeriodicSequence()
    visited: dict[tuple[int, int], list[int]] = collections.defaultdict(list)
    terms, heights = [], []

    tower: Tower = Tower()
    rock_cycler = itertools.cycle(enumerate(ROCKS))
    jet_cycler = itertools.cycle(enumerate(jets))
    rounds = itertools.count()

    while not out.period:
        rock_idx, rock = next(rock_cycler)
        *state, x_left, height = _simulate(rock_idx, rock, tower, jet_cycler)
        visited[tuple(state)].append(next(rounds))
        terms.append(x_left)
        heights.append(height)

        *previous, last = visited[tuple(state)]
        for period1_start, period2_start in itertools.combinations(previous, 2):
            length, period = \
                abs(period1_start - period2_start),\
                terms[period1_start: period2_start]
            if length == abs(period2_start - last) and period == terms[period2_start: last]:
                out.period = length
                out.heights = heights
                out.index_before_first_period = period1_start - 1
                return out
    return


def parse(txt_filename: str) -> str:
    """Return the content of the file as string."""
    return pathlib.Path(txt_filename).read_text()


def _solve(puzzle_input: str, n_rocks: int) -> int:
    periodic_sequence = _determine_period(puzzle_input)
    return periodic_sequence.compute_final_height(n_rocks)


solve_part1 = functools.partial(_solve, n_rocks=2022)
solve_part2 = functools.partial(_solve, n_rocks=1_000_000_000_000)

if __name__ == '__main__':
    title = 'Day 17: Pyroclastic Flow'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The height of the tower after 2022 rocks have stopped falling is {part1}.
        Part 2: The height of the tower after 1^12 rocks have stopped falling is {part2}.
        """)
