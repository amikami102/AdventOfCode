"""
-- Day 20: Grove Positioning System --

Usage example:
    Advent_of_Code/year2022 $ python day20_grove_positioning_system.py day20_test.txt day20_input.txt

The key idea is to not modify the original list of numbers (`encrypted_file`) and instead mix an alternative list, which is a list of the indices so that if the original list is `n` items long, the list that is being mixed consists of (0, 1, 2, ..., n-1). This is better than mixing a copy of encrypted file because the encrypted file can have duplicate integer values. When you're looking for where the item is in the mixed list, it's better to have a unique identifier so that you're moving the right version of the duplicate integer.
"""
import sys
import pathlib
import functools
from typing import *

ZERO = 0
KEY = 811589153
OFFSETS = 1000, 2000, 3000


def _mix(encrypted_file: list[int], repeat: int = 1, decryption_key: int = 1) -> list[int]:
    """
    Mix the items listed in `encrypted_file` by moving each item
    forward or backward by the number of position equal to the integer value of the item.
    """
    n = len(encrypted_file)
    decrypted_order = list(range(n))  # 0, 1, 2, ..., n-1
    # move the `i`th number in `encrypted_file` from position `l` to `k`
    for _ in range(repeat):
        for i, e in enumerate(encrypted_file):
            loc = decrypted_order.index(i)
            del decrypted_order[loc]
            match k := (loc + e * decryption_key) % (n - 1):
                case 0:
                    decrypted_order.append(i)
                case _:
                    decrypted_order.insert(k, i)

    return [encrypted_file[d] * decryption_key for d in decrypted_order]


def _find_grove_coordinates(puzzle_input: list[int], mixer: Callable) -> int:
    """
    Find the number at the offset locations after the value 0 in
    the decrypted file.
    """
    decrypted_file = mixer(puzzle_input)
    zero_index = decrypted_file.index(ZERO)
    return sum(
        decrypted_file[(zero_index + n) % len(decrypted_file)]
        for n in OFFSETS
    )


def parse(txt_filename: str) -> list[int]:
    """Return input file content as a list of integers"""
    return list(map(int, pathlib.Path(txt_filename).read_text().splitlines()))


solve_part1 = functools.partial(_find_grove_coordinates, mixer=_mix)
solve_part2 = functools.partial(
    _find_grove_coordinates,
    mixer=functools.partial(_mix, repeat=10, decryption_key=KEY)
)


if __name__ == '__main__':
    title = 'Day 20: Grove Positioning System'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The sum of the three numbers that form the grove coordinates is {part1}.
        Part 2: The sum of the three numbers that form the grove coordinates is {part2}.
        """)
