# year2024/day07/main.py
import sys
import re 
from typing import Callable
from operator import mul, add
from pathlib import Path 

Equation = tuple[int, ...]
OPERATORS = (mul, add)


def concatenator(x: int, y: int) -> int:
    return int(str(x) + str(y))


def parse_equation(line: str) -> Equation:
    return tuple(int(num) for num in re.findall(r'\d+', line))


def parse(txtfile) -> list[Equation]:
    return [
        parse_equation(line)
        for line in Path(txtfile).read_text().splitlines()
    ] 


def is_calibration_possible(
        equation: Equation, 
        possible_operations: tuple[Callable, ...] = OPERATORS
    ) -> bool:
    """
    Return True if `equation` can be calibrated, otherwise False.
    e.g. 3267: 81 40 27
    target, first, *rest = 3267, 81, (40, 27)
    running = {81}
    y = 40 -> running = {(81) * 40, (81) + 40}
    y = 27 -> running = {(81 * 40) + 27, (81 + 40) * 27}
    """
    target, first, *rest = equation
    running: set[int] = {first}
    for y in rest:
        running = {
            op(x, y)
            for x in running
            if x <= target
            for op in possible_operations 
        }
    return target in running


def solve_part1(data: list[Equation]) -> int:
    return sum(
        equation[0] 
        for equation in data 
        if is_calibration_possible(equation)
    )


def solve_part2(data) -> int:
    return sum(
        equation[0]
        for equation in data 
        if is_calibration_possible(equation, (*OPERATORS, concatenator))
    )


if __name__ == '__main__':
    title = 'Day 7: Bridge Repair'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The total calibration result is {part1}.
        Part 2: The new total calibration result is {part2}.
        """)