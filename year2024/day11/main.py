# year2024/day11/main.py
import sys
from pathlib import Path 
from typing import Iterable, Any
from collections import Counter
from functools import partial


def add_up_counts(tallies: Iterable[tuple[Any, int]]) -> Counter[Any, int]:
    counter = Counter()
    for item, count in tallies:
        counter[item] += count 
    return counter 


def split_stone(stone: int) -> list[int]:
    engraving = str(stone)
    middle = len(engraving) // 2
    return [
        int(engraving[:middle]), 
        int(engraving[middle:])
    ]


def apply_rules(stone: int) -> list[int]:
    engraving = str(stone)
    if engraving == '0':
        return [1]
    elif not len(engraving) % 2:
        return split_stone(stone)
    else:
        return [stone * 2024]
    

def blink(stone_counter: dict[int, int]) -> dict[int, int]:
    return add_up_counts(
        [
            (applied, stone_counter[stone])
            for stone in stone_counter
            for applied in apply_rules(stone)
        ]
    )


def parse(txtfile) -> list[str]:
    return [int(stone) for stone in Path(txtfile).read_text().split()]


def blink_n_times(stones: list[int], n: int) -> int:
    """Return the number of stones in `stones` that result from blinking `n` times."""
    stone_counter = Counter(stones)
    for _ in range(n):
        stone_counter = blink(stone_counter)
    return stone_counter.total()


solve_part1 = partial(blink_n_times, n=25)
solve_part2 = partial(blink_n_times, n=75)


if __name__ == '__main__':
    title = 'Day 11: Plutonium Pebbles'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of stones after blinking 25 times is {part1}.
        Part 2: The number of X-MASes is {part2}.
        """)