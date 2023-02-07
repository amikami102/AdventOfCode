"""
--- Day 20: Grove Positioning System ---

My intuition was similar to this one, so I decided not to do any collections.deque.rotating
or shifting the indices. https://www.reddit.com/r/adventofcode/comments/zqezkn/comment/j0xumzm/?utm_source=share&utm_medium=web2x&context=3
"""
import itertools
import collections
from typing import Iterator, Iterable

with open('day20_input.txt', 'r') as f:
    encrypted: list[int] = list(map(int, f))
ZERO = 0

decrypted_order = list(range(len(encrypted)))     # [ 0, 1, 2, 3, 4, 5, 6]
for i, e in enumerate(encrypted.copy()):
    """Move the ith number of encrypted file e positions right (or left if e < 0) in the decrypted file."""
    if e == 0:
        continue
    loc: int = decrypted_order.index(i)     # 0, 1, 2, ..., or 6
    insertion_loc: int = (loc + e) % (len(encrypted) - 1)
    del decrypted_order[loc]
    decrypted_order.insert(insertion_loc, i) if insertion_loc != 0 else decrypted_order.append(i)
decrypted = [encrypted[d] for d in decrypted_order]
print(
    sum(
        decrypted[(decrypted.index(0) + n) % len(encrypted)] for n in (1000, 2000, 3000)
    )
)