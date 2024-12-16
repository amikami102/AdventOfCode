import sys
from pathlib import Path
from typing import Any, Sequence, Callable
from functools import partial


def parse(txtfile: str) -> list[list[str]]:
    return [
        [tuple(line) for line in paragraph.splitlines()]
        for paragraph in Path(txtfile).read_text().split('\n\n')
    ]


def transpose(matrix: Sequence[Sequence[Any]]) -> Sequence[Sequence[Any]]:
    """Transpose a m x n matrix into n x m matrix."""
    return list(zip(*matrix))


def is_mirror(pattern: list[str], i: int) -> bool:
    """(Part 1)
    Return True if there is a mirror right above row index `i` of `pattern`.
    """
    nrows = min(i, len(pattern) - i)
    above, below = pattern[i - nrows : i], pattern[i: i + nrows ][::-1]
    return above == below


def is_smudged_mirror(pattern: list[str], i: int) -> bool:
    """(Part 2)
    Return True if the rows of `pattern` above (and not including) index `i`
    are mirror reflections of rows below (and including) `i` except for
    exactly one tile.
    """
    nrows = min(i, len(pattern) - i)
    above, below = pattern[i - nrows: i], pattern[i: i + nrows][::-1]
    n_smudges = 0
    for j in range(nrows):
        row1, row2 = above[j], below[j]
        n_smudges += sum(1 for elem1, elem2 in zip(row1, row2) if elem1 != elem2)
        if n_smudges > 1:
            return False
    return n_smudges == 1


def locate_mirror(pattern: list[str], *, mirror_identifier: Callable) -> int:
    """
    Find the row index in `pattern` above which a mirror is located.
    If no mirror is found, return 0.
    """
    for i in range(1, len(pattern)):
        if mirror_identifier(pattern, i):
            return i
    return 0


def solve_part1(puzzle_input: list[list[str]]) -> int:
    mirror_locator = partial(locate_mirror, mirror_identifier=is_mirror)
    return sum(
        mirror_locator(transpose(pattern)) + mirror_locator(pattern) * 100
        for pattern in puzzle_input
    )


def solve_part2(puzzle_input: list[str]) -> int:
    mirror_locator = partial(locate_mirror, mirror_identifier=is_smudged_mirror)
    return sum(
        mirror_locator(transpose(pattern)) + mirror_locator(pattern) * 100
        for pattern in puzzle_input
    )


if __name__ == '__main__':

    title = 'Day 13: Point of incidence'
    print(title.center(50, '-'))

    assert transpose([[1, 2], [3, 4]]) == [(1, 3), (2, 4)]
    assert transpose([('#', '.', '#'), ('.', '#','.')]) == [('#', '.'), ('.', '#'), ('#', '.')]
    assert is_mirror(['###', '###', '...'], 1)
    assert not is_mirror([ '...', '###', '###'], 1)
    assert is_mirror([ '...', '###', '###'], 2)

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The summary number is {part1}.
        Part 2: The summary number of new reflection lines is {part2}.
        """)
