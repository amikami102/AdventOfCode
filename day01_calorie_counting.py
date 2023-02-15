"""
--- Day 1: calorie counting ---

Usage example:
    Advent_of_Code_year_2022 $ python day01.py day01_test.txt day01_input.txt
"""
import sys
import pathlib
import itertools


def parse(txt_filename: str | pathlib.Path) -> list[str]:
    with open(txt_filename, 'r') as f:
        return f.read().splitlines()


def solve_part1(data: list[str]) -> int:
    """
    Group the lines and sum the lines converted into integers.
    Return the largest sum.
    """
    return max(
        sum(int(calories) for calories in sack)
        for is_elf, sack in itertools.groupby(data, key=lambda l: l != '')
        if is_elf
    )


def solve_part2(data: list[str]) -> int:
    """
    Do the same as part1() but return the total of the top 3 largest sums.
    """
    bundles: list[int] = [
        sum(int(calories) for calories in sack)
        for is_elf, sack in itertools.groupby(data, key=lambda l: l != '')
        if is_elf
    ]
    bundles.sort(reverse=True)
    return sum(bundles[:3])


if __name__ == "__main__":
    title = 'Day 01: calorie counting'
    print(title.center(50, '-'))
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(pathlib.Path(path))
        part1 = solve_part1(puzzle_input)
        part2 = solve_part2(puzzle_input)
        print(f'Part 1: The most amount of calories carried by an elf is {part1}.')
        print(f'Part 2: The total calories carried by the top three elves is {part2}.')


