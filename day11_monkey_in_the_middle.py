"""
-- Day 11: Monkey in the Middle --

Usage example:
    Advent_of_Code/year2022 $ python day11_monkey_in_the_middle.py day11_test.txt day11_input.txt


Two lessons:
    1. Taking the common multiple of the monkey's divisors keeps the computation manageable.
    2. When you're changing the data of other items in the list while iterating through the list,
    things get messed up. You can't keep track of the items just by taking their index in enumerate().
    Hash their items out in a separate variable.
"""
import sys
import collections
import re
import operator
import functools
import dataclasses
import math
from typing import *

T = TypeVar('T')
MONKEY_PATTERN: str =\
"""Monkey (.+):
  Starting items: (.+)
  Operation: new = old (.) (.+)
  Test: divisible by (.+)
    If true: throw to monkey (.+)
    If false: throw to monkey (.+)"""
OPERATORS: dict[str, Callable] = {
    '+': operator.add,
    '*': operator.mul
}
Result = collections.namedtuple('Result', ['monkey', 'items'])
Formula = Callable[Sequence, tuple[Result, Result]]


@dataclasses.dataclass
class Monkey:
    id: int
    holding: collections.deque
    operator: Callable
    arg: str
    divisor: int
    true_monkey: int
    false_monkey: int


def parse(txt_filename: str) -> list[Monkey]:
    """
    Read the monkey blocks and return as list of dictionaries containing the following keys: 'id', 'starters', 'operator', 'predicate', 'divisor', 'true_monkey', 'false_monkey'.
    """

    def parse_block(block: str) -> Monkey:
        id, starters, operator, arg, divisor, true_monkey, false_monkey = \
            tuple(*re.findall(MONKEY_PATTERN, block))
        return Monkey(
            id=int(id),
            holding=collections.deque(map(int, starters.split(','))),
            operator=OPERATORS[operator],
            arg=arg,
            divisor=int(divisor),
            true_monkey=int(true_monkey),
            false_monkey=int(false_monkey)
        )

    with open(txt_filename, 'r') as f:
        return [
            parse_block(block)
            for block in f.read().split('\n\n')
        ]


def _simulate(monkeys: list[Monkey], n: int, relief: int = 1) -> int:
    """
    Simulate monkeys passing around the items for n rounds.
    Optionally specify a modifier function to add to monkey formula.
    Return the level of monkey business, which is computed
    by multiplying the top two largest number of items inspected by the monkeys.

    To make computation faster, each monkey's item is reduced to the modulo of mod_all, which is the least common multiple of all the monkey's divisors.
    e.g. If monkey 1's divisor is 3 and monkey 2's divisor is 5, then item value 66 will give the same test results as mod(66, 15) or, equivalently, 6.
    """
    mod_all: int = functools.reduce(
        lambda a, b: a * b,
        (monkey.divisor for monkey in monkeys)
    )
    inspected: collections.Counter[int, int] = collections.Counter()

    # This hashing gives the correct answers.
    items: dict[int, collections.deque] = {
        monkey.id: monkey.holding.copy()
        for monkey in monkeys
    }
    for _ in range(n):
        for monkey in monkeys:
            inspected[monkey.id] += len(items[monkey.id])
            for item in items[monkey.id]:
                arg = item if monkey.arg == 'old' else int(monkey.arg)
                new_item = (monkey.operator(item, arg) % mod_all) // relief
                throw_to = monkey.true_monkey if new_item % monkey.divisor == 0 else monkey.false_monkey
                items[throw_to].append(new_item)
            items[monkey.id].clear()

    return math.prod(v for _, v in inspected.most_common(2))


solve_part1 = functools.partial(_simulate, n=20, relief=3)
solve_part2 = functools.partial(_simulate, n=10000, relief=1)


if __name__ == '__main__':
    title = 'Day 11: Monkey in the Middle'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The level of monkey business after 20 rounds is {part1}.
        Part 2: The level of monkey business after 10000 rounds is {part2}.
        """)
