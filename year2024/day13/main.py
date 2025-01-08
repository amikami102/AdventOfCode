# year2024/day13/main.py
import sys
from typing import Iterator, Optional
from pathlib import Path 
from collections import namedtuple
from numbers import Number
import re 

TOKEN_A, TOKEN_B = 3, 1
CORRECTION = 10000000000000
ClawMachine = namedtuple('ClawMachine', ['ax', 'ay', 'bx', 'by', 'x', 'y'])


def parse_claw_machine(paragraph: str) -> ClawMachine:
    return ClawMachine(
        *[int(number) for number in re.findall(r'\d+', paragraph)]
    )


def correct_conversion_error(claw: ClawMachine) -> ClawMachine:
    x_corrected = claw.x + CORRECTION
    y_corrected = claw.y + CORRECTION
    return claw._replace(x=x_corrected, y=y_corrected)


def parse(txtfile) -> list[str]:
    return Path(txtfile).read_text().split('\n\n')


def is_positive_integer(number: Number) -> bool:
    return number > 0 and not number % 1


def yield_solution(claw: ClawMachine) -> Iterator[tuple[int, int]]:
    """
    Yield the solution to the system of linear equations expressed in `claw`.
    If there is no or infinite number of solutions, yield (0, 0).
    """
    null_solution = (0, 0)
    try:
        bp = (claw.x * claw.ay - claw.y * claw.ax) / (claw.bx * claw.ay - claw.by * claw.ax)
    except ZeroDivisionError:
        return null_solution
    else:
        ap = (claw.x - (claw.bx * bp)) / claw.ax
        if is_positive_integer(ap) and is_positive_integer(bp):
            yield (int(ap), int(bp))


def find_cheapest_solution(solutions: Iterator[tuple[int, int]]) -> int:
    return min(
        (ap * TOKEN_A + bp * TOKEN_B for ap, bp in solutions), 
        default=0
    )


def solve_part1(data) -> int:
    claws = [parse_claw_machine(item) for item in data]
    return sum(
        find_cheapest_solution(yield_solution(claw))
        for claw in claws
    )


def solve_part2(data) -> int:
    claws = [
        correct_conversion_error(parse_claw_machine(item)) 
        for item in data
    ]
    return sum(
        find_cheapest_solution(yield_solution(claw)) 
        for claw in claws
    )


if __name__ == '__main__':
    title = 'Day 13: Claw Contraption'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The fewest number of tokens to win all possible prizes is {part1}.
        Part 2: The correct fewest number of tokens is {part2}.
        """)