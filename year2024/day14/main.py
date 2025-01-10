# year2024/day14/main.py
import sys
from pathlib import Path
from collections import namedtuple, Counter
from typing import Iterable
from functools import reduce
from operator import mul
import re

SECONDS = 100
Robot = namedtuple('Robot', ['x0', 'y0', 'vx', 'vy'])
Coordinate = tuple[int, int]


def parse(txtfile) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def robot_walks(
        robot: Robot,
        floor_width: int = 11,
        floor_length: int = 7
    ) -> Coordinate:
    x, y = robot.x0 + (SECONDS * robot.vx), robot.y0 + (SECONDS * robot.vy)
    return (x % floor_width, y % floor_length)


def count_robots_per_quadrant(
        locations: Iterable[Coordinate],
        floor_width: int = 11,
        floor_length: int = 7
    ) -> Counter:
    x_midpoint, y_midpoint = floor_width // 2, floor_length // 2
    return Counter(
        [
            (x - x_midpoint > 0, y - y_midpoint > 0)
            for x, y in locations
            if x != x_midpoint and y != y_midpoint
        ]
    )


def solve_part1(data: list[str], **kwargs) -> int:
    robots = [
        Robot(
            *[int(num) for num in re.findall(r'-*\d+', item)]
        )
        for item in data 
    ]
    final_locations = (robot_walks(robot, **kwargs) for robot in robots)
    return reduce(
        mul,
        count_robots_per_quadrant(final_locations, **kwargs).values(),
        1
    )


def solve_part2(data):
    pass


if __name__ == '__main__':
    title = 'Day 14: Restroom Redoubt'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        if txtfile == 'input.txt':
            dimension = {'floor_width': 101, 'floor_length': 103}
        else:
            dimension = {}
        part1 = solve_part1(data, **dimension)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The safety factor is {part1}.
        Part 2: The is {part2}.
        """)