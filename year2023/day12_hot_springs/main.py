"""
The recursive solution adapted from David Brownman's solution:
https://advent-of-code.xavd.id/writeups/2023/day/12/, retrieved 2023/01/09.
"""
import sys
from pathlib import Path
from functools import cache

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'


def first_and_only_n_damaged(springs: str, n: int) -> bool:
    """
    Return True if all three conditions are met:
        a) `springs` is at least `n` characters long;
        b) the first `n` characters of `springs` are damaged or unknown;
        c) the next character after the first `n` characters of `springs`
            does not start with DAMAGED.
    """
    return (
        len(springs) >= n
        and all(spring in {DAMAGED, UNKNOWN} for spring in springs[:n])
        and not springs[n:].startswith(DAMAGED)
    )


@cache
def count_arrangements_recursively(springs: str, *damages) -> int:
    """
    Recursively count the ways `springs` fit the numbers of damaged springs
    listed in `damages`.
    """
    if not damages:
        return 0 if springs and '#' in springs else 1
    if not springs:
        return 0 if damages else 1
    
    first_spring, remaining = springs[0], springs[1:]

    if first_spring == OPERATIONAL:
        return count_arrangements_recursively(remaining, *damages)
    if first_spring == DAMAGED:
        n, *damages = damages
        return 0 if not first_and_only_n_damaged(springs, n) else\
            count_arrangements_recursively(springs[n+1:], *damages)
    if first_spring == UNKNOWN:
        start_with_damaged = f'{DAMAGED}{remaining}'
        start_with_operational = f'{OPERATIONAL}{remaining}'
        return count_arrangements_recursively(start_with_damaged, *damages) +\
            count_arrangements_recursively(start_with_operational, *damages)
        

def parse(txtfile: str) -> list[tuple[str, tuple[int, ...]]]:
    return Path(txtfile).read_text().splitlines()


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    springs, groups = line.split()
    return springs, tuple(int(group) for group in groups.split(','))


def unfold(springs: str, records: tuple[int], factor: int = 1) -> tuple[str, tuple[int, ...]]:
    """(Part 2) 
    Replace `springs` with five copies of itself separated by UNKNOWN
    and replace `records` by five copies of itself separated by a comma.
    e.g. '.#', (1) -> '.#?.#?.#?.#?.#', (1, 1, 1, 1, 1)
    """
    return UNKNOWN.join([springs] * factor), records * factor


def solve_part1(puzzle_input: list[str]) -> int:
    record_iterator = (parse_line(line) for line in puzzle_input)
    return sum(
        count_arrangements_recursively(springs, *damages)
        for springs, damages in record_iterator
    )


def solve_part2(puzzle_input: list[str]) -> int:
    record_iterator = (unfold(*parse_line(line), 5) for line in puzzle_input)
    return sum(
        count_arrangements_recursively(springs, *damages)
        for springs, damages in record_iterator
    )


if __name__ == '__main__':

    title = 'Day 12: Hot springs'
    print(title.center(50, '-'))

    assert first_and_only_n_damaged('###', 3)
    assert not first_and_only_n_damaged('####', 3)
    assert not first_and_only_n_damaged('##', 3)

    assert count_arrangements_recursively('###') == 0
    assert count_arrangements_recursively('...') == 1
    assert count_arrangements_recursively('') == 1
    assert count_arrangements_recursively('', 1, 1) == 0
    assert count_arrangements_recursively('.#', 1) == 1
    assert count_arrangements_recursively('.?..', 1) == 1
    assert count_arrangements_recursively('.?..', 1, 2) == 0
    assert count_arrangements_recursively('?.###', 1, 3) == 1
    assert count_arrangements_recursively('???.###', 1, 1, 3) == 1
    assert count_arrangements_recursively('.??#?#????#', 7, 1) == 2

    for filename in sys.argv[1:]:
        data = parse(filename)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{filename}
        Part 1: The total count of all possible arrangements is {part1}.
        Part 2: The sum of the inter-galactic distances post-expansion is {part2}.
        """)
