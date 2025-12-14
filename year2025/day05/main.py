# year2025/day05/main.py
"""
Solution adapted from Reddit user Spinnenente's.
https://github.com/RichRat/pyxercise/blob/3a7e65581c96d2210e73da379f5f592c0beead0d/advent/2025/adv05.py
where they flatten the ranges' start and stop numbers into 
an ordered single sequence of tuple[int, int] whereby  
the second integer equals 1 if the first integer is the 
starting number of a range and -1 if it's the ending number.
e.g. 2-3 and 1-4 would be arranged into 
((1, 1), (2, 1), (3, -1), (4, -1)).
e.g. 1-3, 1-6, and 12-14 would be arranged into 
((1,1), (1,1), (3, -1), (6, -1), (12, 1), (14, -1)).

You can tell a consecutive range ends when the tally of the
second integers of the tuples reaches 0. The range start and
stop are the minimum and maximum of the first integers
observed so far.
"""
from pathlib import Path
from typing import Iterable, Iterator, Collection
from textwrap import dedent
from collections import namedtuple

rangeComponent = namedtuple(
    'rangeComponent', 'number,indicator')

def parse(txtfile: str) -> tuple[list[str], list[str]]:
    [first, second] =  Path(txtfile).read_text().split('\n\n')
    return first.splitlines(), second.splitlines()


def parse_range_line(
        range_line: str) -> Iterator[rangeComponent]:
    start, stop = range_line.split('-')
    yield rangeComponent(int(start), 1)
    yield rangeComponent(int(stop), -1)


def sort_components(
        components: Iterator[rangeComponent]
        ) -> Iterable[rangeComponent]:
    return sorted(components,
        key=lambda component: 
            component.number + 0.3 
            if component.indicator == 1 else 
            component.number + 0.7)


def merge_ranges(
        sorted_components: Iterable[rangeComponent]
        ) -> Collection[tuple[int, int]]:
    merged = []
    start, depth = None, 0
    for component in sorted_components:
        depth += component.indicator
        if start is None and depth==1:
            start = component.number
        if start and depth == 0:
            merged.append((start, component.number))
            start = None
    return merged


def solve_part1(data: tuple[list[str], list[str]]) -> int:
    fresh_para, available_ingredients = data
    fresh_ranges = merge_ranges(
        sort_components(
            component
            for line in fresh_para
            for component in parse_range_line(line)))
    return sum(
        any(low <= int(ingredient) <= high
            for low, high in fresh_ranges)
        for ingredient in available_ingredients
    )
        

def solve_part2(data: tuple[list[str], list[str]]) -> int:
    fresh_para, _ = data
    fresh_ranges = merge_ranges(
        sort_components(
            component
            for line in fresh_para
            for component in parse_range_line(line)))
    return sum(
        high - low + 1
        for low, high in fresh_ranges
    )


if __name__ == '__main__':
    print('%%%%%%%%%%%%%%%%%% day 05: cafeteria %%%%%%%%%%%%%%%%%%')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""\
        part1: the number of fresh, availble ingredients is {part1}.
        part2: the total number of fresh ingredients is {part2}."""))
