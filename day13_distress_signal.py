"""
--- Day 13: Distress Signal ---
"""

import itertools
import collections
import json
from pprint import pprint
from typing import Iterator, Iterable, Sequence


def compare(left: Iterable, right: Iterable) -> bool:
    for l, r in itertools.zip_longest(left, right, fillvalue=None):
        if isinstance(l, int) and isinstance(r, int):
            if l > r:
                return False
            elif l < r:
                return True
            else:
                continue
        elif (l is None) or (r is None):
            if r is None:
                return False
            else:
                return True
        elif isinstance(r, int) and isinstance(l, Iterable):
            return compare(l, [r])
        elif isinstance(l, int) and isinstance(r, Iterable):
            return compare([l], r)
        else:
            return compare(l, r)
    return True


with open('day13_input.txt', 'r') as f:
    pairs = [
        [
            iter(json.loads(packet))
            for packet in pair.split('\n')
        ]
        for pair in f.read().split('\n\n')
    ]

sum_of_indices = sum(
    i+1 for i, pair in enumerate(pairs)
    if compare(*pair)
)
print(f'The sum of indices of pairs that are in order is {sum_of_indices}.')


def bubblesort(arr: list) -> list:
    """
    Implements bubble sort algorithm.
    """
    loop_size = len(arr) - 1
    no_swaps = True

    for i in range(loop_size):
        for j in range(loop_size - i):
            if compare(arr[j], arr[j + 1]):
                continue
            else:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                no_swaps = False
        if no_swaps:
            return arr
    return arr


with open('day13_input.txt', 'r') as f:
    packets = [
        json.loads(packet)
        for pair in f.read().split('\n\n')
        for packet in pair.split('\n')
    ]

packets_sorted = bubblesort(packets)

for divider in ([[2]], [[6]]):
    if compare(divider, packets_sorted[0]):
        packets_sorted.insert(0, divider)
        continue
    for left, right in itertools.pairwise(packets_sorted):
        if compare(left, divider) and compare(divider, right):
            idx = packets_sorted.index(right)
            packets_sorted.insert(idx, divider)
            break

dividers_index_prod = (packets_sorted.index([[2]]) + 1) *(packets_sorted.index([[6]]) + 1)

print(f'The product of divider indices is {dividers_index_prod}.')