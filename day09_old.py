"""
-- Day 09: Rope Bridge --

Usage example:
    Advent_of_Code_2022 $ python day09_rope_bridge.py day09_test.txt day09_input.txt
"""
import sys
import itertools
import collections
from typing import *



class Knot:
    def __init__(self, label):
        self.x, self.y = 0, 0
        self.label = label
        self.history = []

    def write_history(self):
        self.history.append((self.x, self.y))


Head, Tail = Knot('head'), Knot('tail')


def update_tail_coord(tail_knot: Knot, *head_coord) -> None:
    """
    Given the coordinates of the head, update the tail's coordinates so that it is touching the head.
    """
    x, y = head_coord
    dx, dy = x - tail_knot.x, y - tail_knot.y

    if abs(dx) <= 1 and abs(dy) <= 1:
        tail_knot.x += 0
        tail_knot.y += 0
    elif abs(dx) > 1 or abs(dy) > 1:
        tail_knot.x += 1 * int(dx/abs(dx)) if dx != 0 else 0
        tail_knot.y += 1 * int(dy/abs(dy)) if dy != 0 else 0

with open('day09_input.txt', 'r') as f:
    Head.history.append((Head.x, Head.y))
    for line in f:
        direction, steps = line.strip().split(' ')[0], int(line.strip().split(' ')[1])
        for i in range(steps):
            if direction == 'R':
                Head.x += 1
            elif direction == 'L':
                Head.x -= 1
            elif direction == 'U':
                Head.y += 1
            else:
                Head.y -= 1
            Head.write_history()


for coord in Head.history:
    update_tail_coord(Tail, *coord)
    Tail.write_history()

print(f'The tail visits {len(set(Tail.history))} positions.')


knots = [Head, *(knot(str(i+1)) for i in range(9))]


def sliding_window(iterable: Iterable, n: int) -> Iterator:
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for elem in it:
        window.append(elem)
        yield tuple(window)


for pair in sliding_window(knots, 2):
    header, tailer = pair
    for coord in header.history:
        update_tail_coord(tailer, *coord)
        tailer.write_history()

print(f'The tail visits {len(set((knots[-1].history)))} positions at least once.')

