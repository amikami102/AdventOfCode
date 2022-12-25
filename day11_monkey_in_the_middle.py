import re
import collections
from pprint import pprint
import functools
from typing import Sequence

import numpy as np

monkey_patterns = [
    "Monkey (?P<id>\d+):",
    "Starting items: (?P<starters>[\d,\s]+)",
    "Operation: new = old (?P<operator>\W) (?P<predicate>[\d]+|old)",
    "Test: divisible by (?P<divisor>\d+)",
    "If true: throw to monkey (?P<true_monkey>\d+)",
    "If false: throw to monkey (?P<false_monkey>\d+)"
]
part2 = True


def parse_block(block: list[str]) -> dict:
    return {
        k: v
        for line, pattern in zip(block, monkey_patterns)
        for k, v in re.match(pattern, line).groupdict().items()
    }


def manage_worry_level(part2: bool = False):
    if part2:
        def wrapper(holding: Sequence) -> Sequence:
            return holding
    else:
        def wrapper(holding: Sequence) -> Sequence:
            return np.floor(holding / 3).astype(int)

    return wrapper


def define_monkey(modifier: callable, **kwargs) -> callable:
    """
    Define the monkey's inspection formula.
    """
    result = collections.namedtuple('result', ['to', 'items'])

    def formula(holding: Sequence) -> tuple[result, result]:
        holding = np.array(holding)

        if kwargs['operator'] == '*' and kwargs['predicate'] == 'old':
            holding = np.where(holding == 0, 0, holding ** 2)
        elif kwargs['operator'] == '*':
            holding = holding * int(kwargs['predicate'])
        elif kwargs['operator'] == '+':
            holding = holding + int(kwargs['predicate'])
        else:
            raise ValueError(f'unexpected operator {kwargs["operator"]}')

        holding = modifier(holding)
        test_true = int(kwargs['true_monkey']), np.ma.masked_where(
            holding % int(kwargs['divisor']) != 0,
            holding
        ).compressed()
        test_false = int(kwargs['false_monkey']), np.ma.masked_where(
            holding % int(kwargs['divisor']) == 0,
            holding
        ).compressed()

        return result(*test_true), result(*test_false)

    return formula


class Monkey:

    def __init__(self, modifier: callable, **kwargs):
        self.holding = collections.deque([])
        self.inspected = collections.deque([])
        self.holding.extend(
            [int(i) for i in kwargs['starters'].split(', ')]
        )
        self.recipe = define_monkey(modifier, **kwargs)

    @property
    def inspect(self) -> tuple:
        self.inspected.extend(self.holding)
        return self.recipe(self.holding)

    def receive(self, items: list[int]):
        self.holding.extend(items)


with open('day11_input.txt', 'r') as f:
    monkey_recipes = [
        parse_block([line.strip() for line in block.split('\n')])
        for block in f.read().split('\n\n')
    ]

mod_all = functools.reduce(
    lambda prod, x: prod * x,
    [int(recipe['divisor']) for recipe in monkey_recipes]
)
monkeys = [
    Monkey(
        manage_worry_level(part2),
        **recipe
    ) for recipe in monkey_recipes
]


for _ in range(10000):
    for monkey in monkeys:
        true_result, false_result = monkey.inspect
        monkey.holding.clear()
        monkeys[true_result.to].receive(true_result.items.tolist())
        monkeys[false_result.to].receive(false_result.items.tolist())

for monkey in monkeys:
    print(monkey.holding)

tally = [
    len(monkey.inspected) for monkey in monkeys
]
pprint(tally)
tally.sort(reverse=True)
print(f'The level of monkey business after 20 rounds is {tally[0] * tally[1]}.')
