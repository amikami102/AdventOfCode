# python year2024/day01/main.py test.txt
import sys
from typing import Iterable
from pathlib import Path 
from collections import Counter


def map_tuples(iterator: Iterable) -> tuple[int, ...]:
    return tuple(int(item) for item in iterator)

def split_into_two_lists(iterable: Iterable) -> tuple[list, list]:
    return sorted(item for item, _ in iterable), sorted(item for _, item in iterable)
    
def parse(txtfile: str):
    return [
        map_tuples(line.split())
        for line in Path(txtfile).read_text().splitlines()
    ]

def solve_part1(data: list[tuple[int, int]]) -> int:
    llist, rlist = split_into_two_lists(data)
    return sum(
        abs(left - right) 
        for left, right in zip(llist, rlist)
    )

def solve_part2(data: list[tuple[int, int]]) -> int:
    llist, rlist = split_into_two_lists(data)
    rcounter = Counter(rlist)
    return sum(number * rcounter[number] for number in llist)


if __name__ == '__main__':
    title = 'Day 1: Historian Hysteria'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""
        Part 1: The total distance between the two lists is {part1}.
        Part 2: The total similarity score of the two lists is {part2}.
        """)