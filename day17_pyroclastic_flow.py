"""
-- Day 17: Pyroclastic Flow --

Inspired by
    - (very short code) https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day17.py

    - (for a state hashing that's more elegant thant u/juanplopes's) https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0oa5tu/?utm_source=share&utm_medium=web2x&context=3

    - (the most eloquent that uses caching and simulates the rock falling as an overlap between the previous state of the tower
    without the rock and the current state of the tower with the rock)
    https://github.com/Kamik423/advent-of-code-2022/blob/main/17.py

    - (on caching) https://antonz.org/functools-cache/
"""
from typing import Iterable, Iterator
import collections
import itertools
import functools

INITIAL_OFFSET_LEFT: int = 2
INITIAL_OFFSET_TOP: int = 3
CHAMBER_WIDTH: int = 7

CUTOFF_LENGTH: int = 50  # arbitrarily chosen


def convert_to_int(shape: list[str]) -> list[int]:
    """
    Convert the string representation of the shape of the rock into an integer representation
    of the bitarray of the rock as it first appears at the top of the tower.
    e.g. '1111' becomes '0011110' becomes 0b0011110.
    """
    return [
        int(line.zfill(INITIAL_OFFSET_LEFT + len(line)).ljust(CHAMBER_WIDTH, '0'), 2)
        for line in shape
    ]


RIGHT: int = int('1'.zfill(8), 2)  # 0b00000001
LEFT: int = int('1'.ljust(8, '0'), 2)  # 0b1000000
BOTTOM: int = int('1' * 7, 2)  # 0b111111
InnerChamber = tuple[int, ...]
Rock = list[int, ...]
OverlappingPiece = tuple[int, ...]
StateHash = tuple[InnerChamber, int, int]

ROCKS: list[Rock] = list(
        map(
            lambda list_of_str: convert_to_int(list_of_str),
            [
                ['1111'],  # '-' shape
                ['010', '111', '010'],  # '+' shape
                ['111', '001', '001'],  # reverse 'L' shape
                ['1'] * 4,  # 'l' shape
                ['11'] * 2  # 2x2 square shape
            ]
        )
    )
print(ROCKS)

@functools.lru_cache(maxsize=40)
def construct_overlapping_piece(chamber: InnerChamber, rock_index: int) -> OverlappingPiece:
    """
    Construct an overlapping piece whose bottom layer is the chamber itself but replaced by 0's,
    an offset layer of three 0's, and then the next rock about to fall.
    """
    return tuple([0b0000000] * (len(chamber) + INITIAL_OFFSET_TOP) + ROCKS[rock_index])

@functools.lru_cache(maxsize=40)
def simulate_rock_move(chamber: InnerChamber, overlapping_piece: OverlappingPiece, shift_dir: str) -> tuple[bool, OverlappingPiece]:
    """
    Simulate the rock making a move which consists of a single lateral shift and a single drop.
    Return whether the rock can keep moving and the result of the move by updating the shape of the overlapping piece.
    """
    keep_moving: bool = True
    if shift_dir == '>':
        # check whether the shift overlaps with the right wall of the chamber or occupied spaces in the inner chamber
        if all(l >> 1 & RIGHT == 0 for l in overlapping_piece) and all(l >> 1 & cl == 0 for l, cl in zip(overlapping_piece, chamber)):
            overlapping_piece = tuple((layer >> 1 for layer in overlapping_piece))
            print('shifted right', overlapping_piece)
    else:
        # check whether the left shift overlaps with the left wall of the chamber or  occupied spaces in the inner chamber
        if all(l >> 1 & LEFT == 0 for l in overlapping_piece) and all(l << 1 & cl == 0 for l, cl in zip(overlapping_piece, chamber)):
            overlapping_piece = tuple((layer << 1 for layer in overlapping_piece))
    # check whether drop overlaps with the bottom layer or occupied spaces in the chamber
    if all(cl & l == 0 for (cl, l) in itertools.zip_longest((BOTTOM, *chamber), overlapping_piece, fillvalue=0)):
        return keep_moving, overlapping_piece[1:]
    else:
        return not keep_moving, overlapping_piece

@functools.lru_cache(maxsize=40)
def simulate_fall(chamber: InnerChamber, rock_index: int, jet_index: int) -> tuple[StateHash, int]:
    """
    Simulate a rock falling down the chamber until it stops and return a tuple of StateHash and the height added
    to the chamber by the rock fall.
    """
    overlapping_piece: OverlappingPiece = construct_overlapping_piece(chamber, rock_index)
    can_move: bool = True
    while can_move:
        print(overlapping_piece)
        can_move, overlapping_piece = simulate_rock_move(chamber, overlapping_piece, jets[jet_index])
        jet_index = (jet_index + 1) % len(jets)
    chamber_updated: InnerChamber = tuple(
        (cl | l for (cl, l) in itertools.zip_longest(chamber, overlapping_piece, fillvalue=0))
    )
    next_rock_index = (rock_index + 1) % len(ROCKS)
    return (
               chamber_updated[-CUTOFF_LENGTH:],
               next_rock_index,
               jet_index
           ), \
           len(chamber_updated) - len(chamber)

@functools.lru_cache(maxsize=40)
def simulate_through_n_rocks(n_rocks: int, state: StateHash = None) -> tuple[StateHash, int]:
    """
    Simulate n_rocks falling through the chamber.
    """
    chamber_height = 0

    for rock_index in range(n_rocks):
        if state is None:
            state: StateHash = tuple(((), rock_index, 0))
        state, delta_heights = simulate_fall(*state)
        chamber_height += delta_heights
        print(rock_index, state, delta_heights)
    return state, chamber_height




with open('day17_test.txt', 'r') as f:
    jets = f.read().strip()
print(jets[0])

# part 1
_, height = simulate_through_n_rocks(4)
print(height)
# construct_overlapping_piece.cache_clear()
# simulate_through_n_rocks.cache_clear()
# simulate_fall.cache_clear()
# simulate_rock_move.cache_clear()




