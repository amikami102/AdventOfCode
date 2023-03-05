"""
-- Day 21: Monkey Math --

Usage example:
    Advent_of_Code/year2022 $ python day21_monkey_math.py day21_test.txt day21_input.txt

The key idea to solving part 1 (without sympy module) is to use recursion.
For a solution to part 2 that doesn't involve sympy, see this Reddit user's hacky solution that sets
'humn' monkey's integer to 1j. This is similar to algebraically solving the equation except that the symbol is `j`.
https://www.reddit.com/r/adventofcode/comments/zrav4h/comment/j13fuad/?utm_source=share&utm_medium=web2x&context=3
I ultimately adopted using sympy to solve for 'humn' monkey's integer value because the above solution
relies on the assumption that 'humn''s number is not multiplied by itself.
"""
import sys
import pathlib
import operator
import sympy
from typing import *

OPERATORS: dict[str, Callable] = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '=': sympy.Eq   # used in part 2
}
MonkeyJobs = dict[str, tuple[str] | int]


def parse(txt_filename: str) -> MonkeyJobs:
    """
    Return the content of the file as a dictionary of monkey names and their jobs.
    """
    out: MonkeyJobs = {}
    for line in pathlib.Path(txt_filename).read_text().splitlines():
        name, *args = line.replace(':', '').split(' ')
        out[name] = int(next(iter(args))) if len(args) == 1 else tuple(args)
    return out


def recursively_evaluate(jobs: MonkeyJobs, name: str) -> int:
    """
    Recursively evaluate the integer value that is the monkey's job to yell out.
    """
    if not isinstance(jobs[name], tuple):
        return jobs[name]
    else:
        m1, op, m2 = jobs[name]
        return OPERATORS[op](
            recursively_evaluate(jobs, m1),
            recursively_evaluate(jobs, m2)
        )


def solve_part1(puzzle_input: MonkeyJobs) -> int:
    """Return the integer yelled out by the monkey named 'root'."""
    return round(recursively_evaluate(puzzle_input, 'root'))


def solve_part2(puzzle_input: MonkeyJobs) -> int:
    """
    First, update the monkey jobs dictionary by
        - changing 'root' monkey's operation symbol to '='
        - changing 'humn' monkey to sympy.Symbol('humn').
    Return the solution for the integer value of sympy.Symbol('humn') via sympy.solve().
    """
    m1, _, m2 = puzzle_input['root']
    humn = sympy.Symbol('humn')
    jobs_updated = {**puzzle_input, 'root': (m1, '=', m2), 'humn': humn}
    return next(iter(sympy.solve(recursively_evaluate(jobs_updated, 'root'), humn)))




if __name__ == '__main__':
    title = 'Day 21: Monkey Math'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The number yelled out by the monkey named 'root' is {part1}.
        Part 2: The number that I, the monkey named 'humn', have to yell out is {part2}.
        """)
