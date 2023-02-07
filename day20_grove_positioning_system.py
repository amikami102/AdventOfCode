"""
--- Day 20: Grove Positioning System ---

My intuition was similar to this one, so I decided not to do any collections.deque.rotating
or shifting the indices. https://www.reddit.com/r/adventofcode/comments/zqezkn/comment/j0xumzm/?utm_source=share&utm_medium=web2x&context=3
"""
import itertools
import collections
from typing import Iterator, Iterable

with open('day20_input.txt', 'r') as f:
    encrypted = list(map(int, f))

ZERO = 0
KEY = 811589153


def mix(n_mixes: int = 1, decryption_key: int = None):
    if decryption_key is None:
        decryption_key = 1
    decrypted_order = list(range(len(encrypted)))     # [ 0, 1, 2, 3, 4, 5, 6]
    for _ in range(n_mixes):
        for i, e in enumerate(encrypted.copy()):
            if e == 0:
                continue
            loc: int = decrypted_order.index(i)     # 0, 1, 2, ..., or 6
            insertion_loc: int = (loc + e * decryption_key) % (len(encrypted) - 1)
            del decrypted_order[loc]
            decrypted_order.insert(insertion_loc, i) if insertion_loc != 0 else decrypted_order.append(i)

    return [encrypted[d] * decryption_key for d in decrypted_order]


def find_grove_coordinates(*args) -> int:
    decrypted = mix(*args)
    zero_index = decrypted.index(ZERO)
    return sum(
        decrypted[(zero_index + n) % len(decrypted)] for n in (1000, 2000, 3000)
    )


part1 = find_grove_coordinates()
part2 = find_grove_coordinates(10, KEY)
print(part1, part2)