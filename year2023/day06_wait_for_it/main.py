import sys
from typing import *
from pathlib import Path
import re
from math import sqrt, floor, ceil
from operator import mul
from functools import reduce


def extract_integers(string: str) -> tuple[int, ...]:
    return tuple(
        (int(num) for num in re.findall(r'\d+', string))
    )


def parse(filename: str) -> list[list[int]]:
    return [
        extract_integers(line)
        for line in Path(filename).read_text().splitlines()
    ]


def organize_races(times: list[int], distances: list[int]) -> list[tuple[int, int]]:
    return [
        (time_ms, distance_mm) 
        for time_ms, distance_mm in zip(times, distances)
    ]


def organize_race(times: list[int], distances: list[int]) -> tuple[int, int]:
    time = ''.join(str(ms) for ms in times)
    distance = ''.join(str(mm) for mm in distances)
    return int(time), int(distance)


def count_ways_to_win(time_ms: int, distance_mm: int) -> int:
    """
    Let
        t = total time of the race in milliseconds;
        d = longest distance recorded for the race in millimeters;
        h = duration the button is held in milliseconds.
    We want to solve for h such that h * (t - h) > d given the constants (t, d).
    Solving the quadratic inequality, we have
        (1/2) * (t - sqrt(t^2 - 4*d)) < h < (1/2) * (t + sqrt(t^2 - 4*d))
    on the condition that t^2 - 4*d > 0.
    Return the number of whole number h's that satisfy the above condition.
    """
    inside_sqrt = time_ms**2 - 4 * distance_mm
    if inside_sqrt < 0:
        return 0
    else:
        lower = round_to_whole((time_ms - sqrt(inside_sqrt))/2)
        upper = round_to_whole((time_ms + sqrt(inside_sqrt))/2, False)
        return upper - lower + 1


def round_to_whole(decimal: float, lower: bool = True) -> int:
    """
    Round up to the nearest whole number if `lower` is True, down otherwise.
    If there is no decimal (i.e. `decimal % 1 == 0`), 
    then add 1 if `lower`, subtract 1 otherwise.
    e.g. 
        round_to_whole(10.0, True) -> 11
        round_to_whole(20.0, Flase) -> 19
    """
    if lower:
        if decimal % 1:
            return ceil(decimal)
        else:
            return int(decimal + 1)
    else:
        if decimal % 1:
            return floor(decimal)
        else:
            return int(decimal - 1)



def solve_part1(puzzle_input) -> int:
    races = organize_races(*puzzle_input)
    return reduce(
        mul, 
        (count_ways_to_win(time, distance) for (time, distance) in races)
    )

def solve_part2(puzzle_input) -> int:
    one_long_race = organize_race(*puzzle_input)
    return count_ways_to_win(*one_long_race)


if __name__ == '__main__':
    title = 'Day 06: Wait for it'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The product is {part1}.
        Part 2: The number of ways to win this long race is {part2}.
        """)
