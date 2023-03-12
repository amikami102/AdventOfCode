"""
-- Day 05: Supply Stack --

Usage example:
    Advent_Of_Code_/year022 $ python day05_supply_stack.py day05_test.txt day05_input.txt
"""
import sys
import itertools
import collections
import re
from typing import *

Stacks = dict[int, list[str]]
Movement = collections.namedtuple('Movement', ['n', 'from_stack', 'to_stack'])
CRATE_PATTERN = re.compile("\[(?P<letter>[A-Z])\]")
MOVE_PATTERN = re.compile("move (?P<n>[\d]+) from (?P<from>[1-9]) to (?P<to>[1-9])")


def parse_stacks(stack_layers: list[str]) -> Stacks:
    """
    Parse the list of strings into a mapping of stacks listing the stack items from bottom up
    and return the data as Stacks object.
    """
    indices = stack_layers[-1]  # you need to use this function for part 2, so don't pop
    stacks = collections.defaultdict(
        list,
        {int(index): [] for index in indices.split(' ') if index}
    )
    no_crate, blank_crate = ' ' * 4, '[!] '
    for layer in reversed(stack_layers[:-1]):
        crates: list[str] = layer.replace(no_crate, blank_crate).split(' ')
        for i, crate in enumerate(crates):
            crate_letter = re.match(CRATE_PATTERN, crate)
            if crate_letter:
                stacks[i+1].append(crate_letter.group('letter'))
    return stacks


def parse_instructions(instructions: list[str]) -> Iterator[Movement]:
    """
    Given a list of movement statements, parse each statement by matching MOVE_PATTERN
    and extracting the matched groups.
    Yield the tuple of matched substrings as Movement object.
    """
    for line in instructions:
        matched = re.match(MOVE_PATTERN, line)
        yield Movement(int(matched.group('n')), int(matched.group('from')), int(matched.group('to')))


def parse(txt_filename: str) -> tuple[list[str], list[str]]:
    """
    The file content is a 2d view of stacks, an empty line break, and a sequence of movements.
    Use itertools.takewhile() to split the file content into before and after the empty line break (without including the line break).
    """
    it = iter(pathlib.Path(txt_filename).read_text().splitlines())
    stack_layers = [
        line.strip('\n')
        for line in itertools.takewhile(lambda line: line != '\n', it)
        ]
    instructions = [
        line.strip() for line in it
    ]
    return stack_layers, instructions


def solve_part1(initial_stack_layers: list[str], instructions: list[str]) -> str:
    """
    Move the crates according to the instructions. Crates can only be moved one at a time.
    """
    stacks = parse_stacks(initial_stack_layers)
    for move in parse_instructions(instructions):
        for _ in range(move.n):
            crate = stacks[move.from_stack].pop()
            stacks[move.to_stack].append(crate)
    return ''.join(
        stack.pop() for stack in stacks.values()
    )


def solve_part2(initial_stack_layers: list[str], instructions: list[str]) -> str:
    """
    Move the crates according to the instructions.
    Multiple crates are moved at once, but when they are replaced to another stack,
    they retain the same order they were stacked in the original stack.
    """
    stacks = parse_stacks(initial_stack_layers)
    for move in parse_instructions(instructions):
        stacks[move.from_stack], crates = stacks[move.from_stack][:-move.n], stacks[move.from_stack][-move.n:]
        stacks[move.to_stack].extend(crates)
    return ''.join(
        stack.pop() for stack in stacks.values()
    )


if __name__ == '__main__':
    title = 'Day 05: Supply Stacks'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(*data)
        part2 = solve_part2(*data)
        print(f"""{path}:
        Part 1: The crates that end up at the top of the stacks are {part1}.
        Part 2: The crates that end up at the top of the stacks are {part2}.
        """)