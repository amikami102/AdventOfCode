"""
-- Day 21: Monkey Math --

Inspired by
    - (exec() for part 1)
    https://www.reddit.com/r/adventofcode/comments/zrav4h/comment/j12mwt3/?utm_source=share&utm_medium=web2x&context=3

    - u/juanplopes for recursive execution
    https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day21.py

    - (u/sehyod explains why having 'humn' yell 1j works)
    https://www.reddit.com/r/adventofcode/comments/zrav4h/comment/j13fuad/?utm_source=share&utm_medium=web2x&context=3

Part 2 requires you to round to the nearest integer, instead of using int(), which defaults to floor rounding.
"""
from typing import Callable, Any
import operator
import re


OPERATORS: dict[str, Callable] = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
exprs: dict[str, Any] = {}
with open('day21_input.txt', 'r') as f:
    for line in f:
        monkey, *yellout = re.split(r'[\s:]+', line.strip())
        exprs.update({monkey: yellout})


def recursively_evaluate(monkey: str) -> int:
    """
    Recursively evaluate what the monkeys are yelling out.
    """
    yellout = exprs[monkey]
    if len(yellout) > 1:
        m1, op, m2 = yellout
        return OPERATORS[op](
            recursively_evaluate(m1),
            recursively_evaluate(m2)
        )
    else:
        return complex(yellout[0])


# part 1
part1 = round(recursively_evaluate('root').real)
print(part1)
# part 2
exprs = exprs | {'humn': [1j]}
m1, _, m2 = exprs['root']
exprs = exprs
lh = recursively_evaluate(m1)
rh = recursively_evaluate(m2)
print(round((lh.real-rh.real)/(rh.imag - lh.imag)))