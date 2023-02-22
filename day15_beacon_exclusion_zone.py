"""
-- Day 15: Beacon Exclusion Zone --

Usage example:
    Advent_of_Code/year2022 $ python day15_beacon_exclusion_zone.py day15_test.txt day15_input.txt


Inspired by Peter Norvig's solution:

Part 1:
Do not find all sensor detector ranges but limit the search within the target y coordinate region.

Part 2:
The main idea is illustrated by this reddit user's diagram. https://www.reddit.com/r/adventofcode/comments/zmcn64/comment/j0j289z/?utm_source=share&utm_medium=web2x&context=3
The target beacon is located outside all sensors' ranges. Since this is the only such beacon, the beacon must lie
    - above one sensor's upper right edge,
    - another sensor's upper left edge,
    - below a third sensor's lower right edge,
    - and below a fourth sensor's lower left edge.
So the steps to the solution are:
    1. Draw points along the line segments 1 unit above/below detection edges of each sensor.
    2. Filter out points whose x or y coordinate is outside [0, 4_000_000] or is detectable by a sensor.
You should be left with one intersection point by the end of step 2.

The above solution to part 2 takes longer than this solution, which involves more intermediate steps between 1 and 2.
    A1. Draw the perimeter edges like step 1.
    A2. Filter out edges that are not shared by at least 2 sensors.
    A3. Find the intersection point for every pair of edges.
    A4. Filter out intersection points whose x or y coordinate is outside [0, 4_000_000] or is detectable by some sensor.
"""
import sys
import pathlib
import functools
import re
import collections
import operator
import itertools
from typing import *

Coord = tuple[int, int]     # (x, y)
Vector = Coord
SensorBeacon = collections.namedtuple('SensorBeacon', ['Sensor', 'Beacon'])

INTEGER_PATTERN = re.compile('-?[0-9]+')
X, Y = 0, 1
DIAGONALS = NW, NE, SW, SE = (-1, -1), (1, -1), (-1, 1), (1, 1)


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[X] + vector2[X], vector1[Y] + vector2[Y]


def _manhattan_distance(coord1: Coord, coord2: Coord) -> int:
    return abs(coord1[X] - coord2[X]) + abs(coord1[Y] - coord2[Y])


def parse(txt_filename: str) -> list[SensorBeacon]:
    """
    Return each line as SensorBeacon class object.
    e.g. "Sensor at x=155404, y=2736782: closest beacon is at x=2062250, y=2735130"
    becomes `SensorBeacon(Sensor=(155404, 2736782), Beacon=(2062250, 2735130))`.
    """
    return [
        SensorBeacon(
            tuple(map(int, INTEGER_PATTERN.findall(line.split(':')[0]))),
            tuple(map(int, INTEGER_PATTERN.findall(line.split(':')[1])))
        )
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


def _count_empty_coords(pairs: list[SensorBeacon], yline: int = 10) -> int:
    """
    (Part 1)
    Count known coordinates on y = y_line that we know cannot have a beacon.
    Make sure to exclude any beacon located on y_line.
    """

    def _mark_empty_coords(sensor: Coord, beacon: Coord) -> Iterator[int]:
        """
        Return a range of coordinates on Y = y_line that definitely do not have a beacon according to the sensor-beacon pair. Only return the X coordinate values.
        """
        radius: int = _manhattan_distance(sensor, beacon)
        height: int = abs(yline - sensor[Y])
        if height > radius:  # yline is outside of sensor radius
            return range(0, 0)  # empty range
        else:
            x_left, x_right = sensor[X] - (radius - height), \
                              sensor[X] + (radius - height)
            return range(x_left, x_right + 1)  # return x from [x_left, x_right]

    empty_coords = {x for pair in pairs for x in _mark_empty_coords(*pair)} \
        - {beacon[X] for _, beacon in pairs if beacon[Y] == yline}
    return len(empty_coords)


def _find_distress_beacon(sb_pairs: list[SensorBeacon], max_value: int = 20):
    """
    (Part 2)
    Find the distress beacon, which is between 0 and the value of y_max in both its x and y coordinate values AND is undetected by all the sensors.
    Return the distress signal of the beacon.
    """

    def _draw_above_below_sensor_edge(sensor: Coord, beacon: Coord) -> Iterator[Coord]:
        """
        Yield point drawn from the perimeter 1 unit around the sensor's detection range.
        """
        radius: int = _manhattan_distance(sensor, beacon) + 1
        point: Coord = _add_vectors(sensor, (0, -radius))  # start at northernmost point
        yield from itertools.accumulate(
            (
                r
                for direction in (SE, SW, NW, NE)
                for r in itertools.repeat(direction, radius)
            ),
            func=_add_vectors,
            initial=point
        )

    def _disqualified(point: Coord) -> bool:
        """
        Return True if
        - the point's x or y coordinate is outside [0, max_value]
        - the point is within some sensor's detection range of a sensor.
        """
        return 0 > min(point) or\
            max(point) > max_value or \
            any(
                _manhattan_distance(point, sensor) <= _manhattan_distance(sensor, beacon)
                for sensor, beacon in sb_pairs
            )

    target_beacon = next(
        p
        for pair in sb_pairs
        for p in _draw_above_below_sensor_edge(*pair)
        if not _disqualified(p)
    )
    return target_beacon[X] * 4_000_000 + target_beacon[Y]


if __name__ == '__main__':
    title = 'Day 15: Beacon Exclusion Zone'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        if 'test' in path:
            solve_part1 = _count_empty_coords
            solve_part2 = _find_distress_beacon
        else:
            solve_part1 = functools.partial(_count_empty_coords, yline=2_000_000)
            solve_part2 = functools.partial(_find_distress_beacon, max_value=4_000_000)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The number of positions that cannot contain a beacon is {part1}.
        Part 2: The distress signal is {part2}.
        """)
