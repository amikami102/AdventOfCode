# year2024/day05/main.py
import sys 
from itertools import combinations
from pathlib import Path
from functools import cmp_to_key


def parse_rules(rules_section: str) -> list[tuple[int, int]]:
    return [
        tuple(int(num) for num in rule.split('|'))
        for rule in rules_section.split()
    ]


def parse_updates(updates_section: str) -> list[tuple[int, ...]]:
    return [
        tuple(int(num) for num in update.split(','))
        for update in updates_section.split()
    ]


def parse(txtfile: str) -> tuple[list, list]:
    sec1, sec2 = Path(txtfile).read_text().split('\n\n')
    return parse_rules(sec1), parse_updates(sec2)


def is_incorrect_order(
        update: tuple[int, ...],
        rules: list[tuple[int, int]]
    ) -> bool:
    """
    An update is in incorrect order if any of its two pages explicitly break a rule.
    """
    return any(
        (p2, p1) in rules
        for p1, p2 in combinations(update, 2)
    )


def get_middle_page(pages: list[int]) -> int:
    return pages[len(pages) // 2]


def solve_part1(data) -> int:
    """Take the sum of the middle pages of updates that are in corret order."""
    rules, updates = data
    return sum(
        get_middle_page(update)
        for update in updates 
        if not is_incorrect_order(update, rules)
    )


def solve_part2(data):
    """
    Reorder the sequence of incorrect updates and take
    the sum of the middle pages.
    """
    rules, updates = data
    @cmp_to_key
    def order_pages(page1, page2) -> int:
        if (page1, page2) in rules:
            return 1
        elif (page2, page1) in rules:
            return -1 
        else:
            return 0
    return sum(
        get_middle_page(sorted(update, key = order_pages))
        for update in updates 
        if is_incorrect_order(update, rules)
    )


if __name__ == '__main__':
    title = 'Day 5: Print Queue'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The sum of the middle pages of correctly ordered updates is {part1}.
        Part 2: The sum of the middle pages of corrected updates is {part2}.
        """)