"""
 Day 15: Beacon Exclusion Zone
"""
from typing import Iterator, Iterable, NamedTuple
import re
import collections
import itertools


Line = collections.namedtuple('Line', ['slope', 'intercept'])

class Segment:
    """A class holding a segment of consecutive integers."""
    def __init__(self, *args):
        self.start, self.stop = min(*args), max(*args)
        self.width = abs(self.start - self.stop) + 1

    def __repr__(self):
        return f'Segment(start={self.start}, stop={self.stop})'

    def overlaps(self, other) -> bool:
        return self.stop >= other.start or self.start >= other.stop

    def __lt__(self, other) -> bool:
        return self.start < other.start


line_pattern = re.compile(
    'Sensor at x=(?P<x>-*\d+), y=(?P<y>-*\d+): closest beacon is at x=(?P<beacon_x>-*\d+), y=(?P<beacon_y>-*\d+)'
)

Beacon = collections.namedtuple('Beacon', ['x', 'y'])


class Sensor:
    """
    A class representing a sensor.

    Attributes:
        line : str (string representation)
        x, y: int, int (point coordinate of the sensor)
        nearestBeacon: beacon (the nearest beacon detected by the sensor)
        distance: int (the Manhattan distance between the nearest beacon and the sensor)

    Methods:
        sense_range(row: int) -> list[Segment]
            Return a list of Segmentg containing the range of x's that the sensor can detect if the given row is
            within the sensor's range, otherwise return None

        detect_point(point: tuple[int, int]) -> bool
            Return True if a given point is within the sensor's detection range, otherwise False

        draw_boundary_lines(None) -> Iterator[Line]:
            Yield the four Lines bounding the sensor's detection range
    """

    def __init__(self, **kwargs):
        self.x, self.y = int(kwargs['x']), int(kwargs['y'])
        self.nearestBeacon = Beacon(x=int(kwargs['beacon_x']), y=int(kwargs['beacon_y']))
        self.distance = abs(self.nearestBeacon.x - self.x) + abs(self.nearestBeacon.y - self.y)

    def __repr__(self):
        return f'Sensor(x={x}, y={y})'

    def sense_range(self, y: int) -> list[Segment]:
        ranges = []
        x_leg = self.distance - abs(self.y - y)
        if x_leg > 0:
            start, stop = self.x - x_leg, self.x + x_leg
            if self.nearestBeacon.y == y:
                if self.nearestBeacon.x == start:
                    start += 1
                else:
                    stop -= 1
            if self.y == y:
                ranges.extend(
                    [
                        Segment(start, self.x - 1),
                        Segment(self.x + 1, stop)
                    ]
                )
            else:
                ranges.append(Segment(start, stop))
        return ranges

    def detect_point(self, point: tuple[int, int]) -> bool:
        x, y = point
        return abs(self.x - x) + abs(self.y - y) <= self.distance

    def draw_boundary_lines(self) -> Iterator[Line]:
        yield from (
            Line(1, self.y - (self.x - self.distance - 1)),
            Line(-1, self.y + (self.x - self.distance - 1)),
            Line(1, self.y - (self.x + self.distance + 1)),
            Line(-1, self.y + (self.x + self.distance + 1))
        )


def parse_line(line: str) -> dict:
    """Parse line by applying regex matching and construct a Sensor object."""
    matched = re.match(line_pattern, line)
    return matched.groupdict()


def merge_overlapping_segments(segment_list: Iterable[Segment]) -> Iterator[Segment]:
    """
    Given a list of Segments, merge any pair of line segments that overlap.
    Return a list of non-overlapping segments.
    """
    head = None
    for seg in sorted(segment_list):
        if head is None:
            head = seg
        if head.overlaps(seg):
            head = Segment(
                min(head.start, seg.start),
                max(head.stop, seg.stop)
            )
            continue
        else:
            yield head
            head = seg
    yield head


def find_intersection(line1: Line, line2: Line) -> tuple[int, int] | None:
    """
    Find the intersection between two Lines.
    If line1 and line2 have the same slope values, return None.
    """
    if line1.slope == line2.slope:
        return None
    else:
        x = - (line1.intercept - line2.intercept) // (line1.slope - line2.slope)
        y = line1.slope * x + line1.intercept
        return x, y


def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for elem in it:
        window.append(elem)
        yield tuple(window)


with open('day15_input.txt', 'r') as f:
    sensors = [
        Sensor(**parse_line(line)) for line in f
    ]

# part 1
target_row = 2000000 #10
sensible_ranges = itertools.chain(
    *[
        sensor.sense_range(target_row)
        for sensor in sensors
        if sensor.sense_range(target_row)
    ]
)
merged = merge_overlapping_segments(sorted(sensible_ranges))
known_empty = sum(abs(seg.start - seg.stop) + 1 for seg in merged)
print(f'Row y={target_row} has {known_empty:,} positions that cannot contain a beacon.')


# part 2
lower, upper = 0, 4000000
lines = collections.Counter(
    itertools.chain(*(sensor.draw_boundary_lines() for sensor in sensors))
)
filtered = (
    line for line, cnt in lines.items() if cnt >= 2
)
intersections = filter(
    lambda pt: pt is not None and lower <= pt[0] <= upper and lower <= pt[1] <= upper,
    (
        find_intersection(*pair)
        for pair in itertools.combinations(filtered, 2)
    )
)

for p in intersections:
    if any(sensor.detect_point(p) for sensor in sensors):
        continue
    else:
        tuning_freq = 4000000 * p[0] + p[1]
        print(f'The only possible position for the distress beacon is at tuning frequency {tuning_freq}.')
        break





