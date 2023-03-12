"""
--- Day 1: calorie counting ---

Usage example:
    Advent_Of_Code/year2022 $ python day01.py day01_test.txt day01_input.txt
"""
import sys
import pathlib
import itertools


def parse(txt_filename: str) -> list[str]:
    return pathlib.Path(txt_filename).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    """
    Group the lines and sum the lines converted into integers.
    Return the largest sum.
    """
    return max(
        sum(int(calories) for calories in sack)
        for is_elf, sack in itertools.groupby(puzzle_input, key=lambda l: l != '')
        if is_elf
    )


def solve_part2(puzzle_input: list[str]) -> int:
    """
    Return the total of the top 3 largest sums.
    """
    bundles: list[int] = [
        sum(int(calories) for calories in sack)
        for is_elf, sack in itertools.groupby(puzzle_input, key=lambda l: l != '')
        if is_elf
    ]
    bundles.sort(reverse=True)
    return sum(bundles[:3])


if __name__ == "__main__":
    title = 'Day 01: calorie counting'
    print(title.center(50, '-'))

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{file}:
        Part 1: The most amount of calories carried by an elf is {part1}.
        Part 2: The total calories carried by the top three elves is {part2}.
        """)



