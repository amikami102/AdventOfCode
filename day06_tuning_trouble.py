"""
-- Day 06: Tuning Trouble --

Usage example:
    Advent_of_Code/year2022 $ python day06_tuning_trouble.py day06_test.txt day06_input.txt
"""
import sys
from typing import *
import itertools
import functools
import collections
T = TypeVar('T')


def parse(txt_filename: str) -> str:
    """Return the one line of strings in the txt file"""
    with open(txt_filename, 'r') as f:
        return f.readline()


def _solve(line: str, n_char: int = 4) -> int:
    """
    Iterate through the line and return the index of the first character
    after the most recent n_char string characters that are all unique.
    """
    def sliding_window(iterable: Iterable[T], n: int) -> Iterator[collections.deque[T]]:
        it = iter(iterable)
        window = collections.deque(itertools.islice(it, n), maxlen=n)
        for item in it:
            window.append(item)
            if len(tuple(window)) == n:
                yield tuple(window)
        yield tuple(window)

    windows = sliding_window(line, n_char)

    return next(itertools.dropwhile(
        lambda entry: len(set(entry[1])) < n_char,
        enumerate(sliding_window(line, n_char))
    ))[0] + n_char + 1


solve_part1: Callable = functools.partial(_solve, n_char=4)
solve_part2: Callable = functools.partial(_solve, n_char=14)

if __name__ == '__main__':
    title = 'Day 06: Tuning Trouble'
    print(title.center(50, '-'))
    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The number of characters that need to be processed before the first start-of-the-parket marker is detected is {part1}.
        Part 2: The number of characters that need to be processed before the first start-of-the-message marker is detected is {part2}.
        """)
