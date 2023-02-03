"""
-- Day 17: Pyroclastic Flow --

Inspired by
    - (very short code that uses hashing)
     https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day17.py

    - (for a state hashing that's more elegant thant u/juanplopes's) https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0oa5tu/?utm_source=share&utm_medium=web2x&context=3

    - (the most eloquent that uses caching and simulates the rock falling as an overlap between the previous state of the tower
    without the rock and the current state of the tower with the rock)
    https://github.com/Kamik423/advent-of-code-2022/blob/main/17.py

    - (on caching) https://antonz.org/functools-cache/

    - (the most simple but eloquent)
    https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0vj0l2/?utm_source=share&utm_medium=web2x&context=3
"""
from typing import Iterable, Iterator
import collections
import itertools

INITIAL_OFFSET_LEFT: int = 2
INITIAL_OFFSET_TOP: int = 3
CHAMBER_WIDTH: int = 7


def convert_to_int(shape: list[str]) -> list[int]:
    """
    Convert the string representation of the shape of the rock into an integer representation
    of the bitarray of the rock as it first appears at the top of the tower.
    e.g. '1111' becomes '0011110' becomes 0b0011110.
    """
    return [
        int(line.ljust(CHAMBER_WIDTH, '0'), 2)
        for line in shape
    ]


Rock = list[int, ...]
innerChamber: list[int] = []
heightSequence: list[int] = []
Rounds = collections.defaultdict(list)
dxSequence: list[int] = []
lastIndexBeforeFirstPeriod: int = 0
periodLength: int = 0
deltaHeightPerPeriod: int = 0


def fits(cur_rock: Rock, dx: int, depth: int) -> bool:
    """
    This function is encountered only when dy > 0.
    Check whether the rock can be transposed by dx units in the x direction
        by confirming that rock >> dx << dx keeps the original rock shape intact.
        - If rock >> dx spills over the chamber width, the original shape cannot be recovered by << dx.
            This tells us that the rock shouldn't be shifted by dx units.
        - It starts with >> because the rock must be right-shifted INITIAL_OFFSET_LEFT units when it
        first appears.
        - Not in this function, but dx will be an integer within [0, 7] because you can't right-shift by negative units and the most distance that the leftmost 1 can be shifted is 7 units.
    Check whether the rock can be transposed by dx units laterally AND dy units down
        by confirming that the j-th row from the bottom of the chamber has no intersection with (j-dy)th row of the Rock.
        - dy represents the number of rows from the bottom of the chamber where the Rock's bottom row will be placed if this move works.
        - The condition is not triggered if len(Chamber) == 0 because range(dy, 0) returns an empty iterator
            or if len(Chamber) > 0 but len(Chamber) < y because range(y, len(Chamber)) returns an empty iterator.
        - The condition is triggered for the first time when the iterator is non-empty,
            i.e. when y = len(chamber) - 1. This is when we're testing whether the bottom of the Rock can pass
           the topmost row of the Chamber. In that case, the iterator is range(y, y+1).

        Here's what's happening visually when dy = len(chamber) - 1, dx=0, for a '-'-shaped rock.
        chamber[len(chamber) - 1]   |...#...|       |..####...|     rock[0]     j = len(chamber) - 1
                                        ...
        chamber[2]                  |..###..|
        chamber[1]                  |...#...|
        chamber[0]                  |..####.|
                                    +-------+
        - Once the Rock passes the topmost row of the len(Chamber), i.e. y < len(Chamber) - 1,
            we want to check the portion of the Rock that overlaps with the Chamber, which
            might stop short of the topmost row of the Chamber, hence min(len(Chamber), y + len(Rock)).

        Here's what's happening visually when dy = len(chamber) - 2, dx = 0, for a square rock.
        chamber[len(chamber) - 1]   |#......|       |..##...|   rock[1]     j = len(chamber) - 1
        chamber[len(chamber) - 2]   |#......|       |..##...|   rock[0]     j = len(chamber) - 2
                                        ...
        chamber[2]                  |..###..|
        chamber[1]                  |...#...|
        chamber[0]                  |..####.|
                                    +-------+
        Here's what's happening visually when dy = 3, dx = 0, for a square rock.
        chamber[len(chamber) - 1]   |#......|
                                        ...
        chamber[4]                  |......#|       |..##...|   rock[1]     j = 4 = dy + len(rock) - 1
        chamber[3]                  |......#|       |..##...|   rock[0]     j = 3
        chamber[2]                  |..###..|
        chamber[1]                  |...#...|
        chamber[0]                  |..####.|
                                    +-------+

    """
    if not (depth > 0 and 0 <= dx <= 7):
        assert ValueError('dy and dx out of bounds')
    lateral_shift_keeps_rock_intact: bool = all(line >> dx << dx == line for line in cur_rock)
    lateral_shift_and_drop_has_no_intersection: bool = not any(
        innerChamber[j] & cur_rock[j - depth] >> dx
        for j in range(
            depth,
            min(len(innerChamber), depth + len(cur_rock))
        )
    )
    return lateral_shift_keeps_rock_intact and lateral_shift_and_drop_has_no_intersection


def compute_final_height(n_rocks: int):
    """
    As soon as periodLength variable is nonzero, this function will be triggered to
    determine the final height of innerChamber after n_rocks have fallen through the chamber.
    """
    n_periods, remainder = divmod(n_rocks - lastIndexBeforeFirstPeriod, periodLength)
    return deltaHeightPerPeriod * n_periods + \
        heightSequence[(lastIndexBeforeFirstPeriod + remainder) - 1]


ROCKS: list[Rock] = list(
    map(
        lambda list_of_str: convert_to_int(list_of_str),
        [
            ['1111'],  # '-' shape
            ['010', '111', '010'],  # '+' shape
            ['111', '001', '001'],  # reverse 'L' shape
            ['1'] * 4,  # 'l' shape
            ['11'] * 2  # 2x2 square shape
        ]
    )
)

with open('day17_input.txt', 'r') as f:
    jets = f.read().strip()

rock_cycler: Iterator[list] = itertools.cycle(enumerate(ROCKS))
jet_cycler: Iterator[str] = itertools.cycle(enumerate(jets))

while not periodLength:
    rock_index, rock = next(rock_cycler)
    dx, depth = 2, len(innerChamber) + 4
    jet_index, jet = None, None
    while depth and fits(rock, dx, depth - 1):
        depth -= 1
        jet_index, jet = next(jet_cycler)
        new_dx = max(0, dx - 1) if jet == '<' else min(7, dx + 1)
        dx = new_dx if fits(rock, new_dx, depth) else dx

    for j, rock_line in enumerate(rock, start=depth):
        if j < len(innerChamber):
            innerChamber[j] |= rock_line >> dx
        else:
            innerChamber.append(rock_line >> dx)
    heightSequence.append(len(innerChamber))
    dxSequence.append(dx)
    Rounds[(rock_index, jet_index)].append(len(dxSequence))

    *previous, current_round = tuple(Rounds[rock_index, jet_index])
    """
        The following will be triggered when you have a third round added to Rounds[repeating_index]
        and returns nothing if you fail to determine the repeating_index is the beginning of a period.
    """
    for b, m in itertools.combinations(previous, 2):
        if abs(b - m) == abs(m - current_round) and dxSequence[b:m] == dxSequence[m:]:
            lastIndexBeforeFirstPeriod, periodLength, deltaHeightPerPeriod = \
               b - 1, \
               abs(m - b), \
               len(innerChamber) - heightSequence[m - 1]

print('part 1: ', compute_final_height(2022))
print('part 2: ', compute_final_height(1000000000000))
