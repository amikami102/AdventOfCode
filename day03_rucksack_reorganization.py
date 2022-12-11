"""
-- Day 04 rucksack reorganization ---
The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items
vJrwpWtwJgWr,
while the second compartment contains the items
hcsFMMfFFhFp.
The only item type that appears in both compartments is lowercase p.
The second rucksack's compartments contain
jqHRNqRjqzjGDLGL
and
rsFMfFZSrLrFZsSL.
The only item type that appears in both compartments is uppercase L.
The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
The fourth rucksack's compartments only share item type v.
The fifth rucksack's compartments only share item type t.
The sixth rucksack's compartments only share item type s.
To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is
16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack.
What is the sum of the priorities of those item types?
"""
import string

priority_lookup = {
    letter: val + 1
    for val, letter in enumerate([*string.ascii_lowercase, *string.ascii_uppercase])
}

priorities = []
with open('day03_input.txt', 'r') as f:
    for rucksack in f:
        first, second = set(rucksack[:len(rucksack) // 2]), set(rucksack[len(rucksack) // 2:])
        common = first.intersection(second).pop()
        priorities.append(priority_lookup[common])

print(f'The sum of priorities is {sum(priorities):,}.')

"""
Every set of three lines in your list corresponds to a single group, 
but each group can have a different badge item type.
So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. 
In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: 
here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. 
What is the sum of the priorities of those item types?
"""

import itertools

badges = []
with open('day03_input.txt', 'r') as f:
    args = [iter(f)] * 3  # inspired by "grouper" function recipe on itertools doc
    for group in itertools.zip_longest(*args, fillvalue=None):
        first, second, third = group
        common = set(first.strip()) \
            .intersection(set(second.strip())) \
            .intersection(set(third.strip())).pop()
        badges.append(priority_lookup.get(common, 0))

print(f'The sum of the priorities is {sum(badges):,}.')
