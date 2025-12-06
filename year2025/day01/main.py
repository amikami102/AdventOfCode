#year2025/day01/main.py
from textwrap import dedent
from pathlib import Path
from typing import Iterable

START = 50
MODULUS = 100

def parse(txtfile: str) -> Iterable[str]:
    return Path(txtfile).read_text().splitlines()


def parse_rotation(rotation: str) -> tuple[str, int]:
    return rotation[0], int(rotation[1:]) 


def turn(current: int, direction: str, distance: int) -> int:
    """
    Turn a dial numbered 0 through 99 from `current` position 
    in `direction` for `distance` clicks.
    Return the final position.

    n.b. distance of 100 will make full rotation
    """
    return (current + distance) % MODULUS \
        if direction.lower() == 'r' else \
        (current - distance) % MODULUS


def solve_part1(rotations: Iterable[str]) -> int:
    """Count the number of times the dial ends at 0 after a rotation."""
    zeros, current = 0, START
    for rotation in rotations:
        current = turn(current, *parse_rotation(rotation))
        if current == 0:
            zeros += 1
    return zeros


def count_passes_through_zero(
        current: int, direction: str, distance: int) -> int:
    if direction.lower() == 'r':
        return (current + distance) // MODULUS
    else:
        if current == 0:
            return distance // MODULUS
        elif distance >= current:
            return (distance - current) // MODULUS + 1
        else:
            return 0


def solve_part2(rotations: Iterable[str]) -> int:
    """
    Count the number of times the dial points at 0 during a rotation including when the rotation is complete.
    """
    zeros, current = 0, START
    for rotation in rotations:
        direction, distance = parse_rotation(rotation)
        zeros += count_passes_through_zero(
            current, direction, distance)
        current = turn(current, direction, distance)
    return zeros


if __name__ == '__main__':
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""\
        ++++++++ day 01: secret entrance ++++++++++++
        Part 1: the password to the secret entrance is {part1}.
        Part 2: the password under the new protocol is {part2}.
        """))
    