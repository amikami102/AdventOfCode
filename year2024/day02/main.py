# year2024/day02/main.py
from typing import Iterable
import sys
from pathlib import Path
from itertools import pairwise

MIN_DIFFERENCE = 1
MAX_DIFFERENCE = 3


def parse(txtfile: str) -> list[list[int]]:
    return [
        [int(num) for num in line.split()]
        for line in Path(txtfile).read_text().splitlines()
    ]


def is_strictly_increasing(delta1: int, delta2: int) -> bool:
    return delta1 > 0 and delta2 > 0


def is_strictly_decreasing(delta1: int, delta2: int) -> bool:
    return delta1 < 0 and delta2 < 0


def is_gradual(diff1: int, diff2: int) -> bool:
    return (MIN_DIFFERENCE <= abs(diff1) <= MAX_DIFFERENCE) and\
    (MIN_DIFFERENCE <= abs(diff2) <= MAX_DIFFERENCE)


def is_safe_report(report: Iterable[int]) -> bool:
    first_differential = (
        pair[1] - pair[0] for pair in pairwise(report)
    )
    for deltas in pairwise(first_differential):
        if is_strictly_increasing(*deltas) and is_gradual(*deltas):
            continue
        elif is_strictly_decreasing(*deltas) and is_gradual(*deltas):
            continue
        else:
            return False
    return True


def is_tolerably_safe(report: Iterable[int], test_level=0) -> bool:
    if test_level >= len(report):
        return False
    else:
        test_report = (
            value
            for level, value in enumerate(report)
            if level != test_level
        )
        if is_safe_report(test_report):
            return True
        else:
            return is_tolerably_safe(report, test_level + 1)


def solve_part1(data) -> int:
    return sum(is_safe_report(report) for report in data)


def solve_part2(data) -> int:
    return sum(
        is_safe_report(report) or is_tolerably_safe(report)
        for report in data
    )


if __name__ == '__main__':
    title = 'Day 2: Red-Nosed Reports'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of safe reports is {part1}.
        Part 2: The number of tolerably safe reports is {part2}.
        """)