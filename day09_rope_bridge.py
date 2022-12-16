"""
Simulate your complete hypothetical series of motions.
How many positions does the tail of the rope visit at least once?
"""
from pprint import pprint
import itertools
import collections
from typing import Iterable, Iterator, Tuple


class knot:
    def __init__(self, label):
        self.x, self.y = 0, 0
        self.label = label
        self.history = []

    def write_history(self):
        self.history.append((self.x, self.y))


Head, Tail = knot('head'), knot('tail')


def update_tail_coord(tail_knot: knot, *head_coord) -> None:
    """
    Given the coordinates of the head, update the tail's coordinates so that it is touching the head.
    """
    x, y = head_coord
    x_distance = x - tail_knot.x
    y_distance = y - tail_knot.y

    if abs(x_distance) <= 1 and abs(y_distance) <= 1:
        tail_knot.x += 0
        tail_knot.y += 0
    elif abs(x_distance) > 1 or abs(y_distance) > 1:
        #print(tail_knot.history)
        #raise ValueError(f'The head ({x, y}) moved too fast from the tail ({tail_knot.x, tail_knot.y})')
    #elif abs(x_distance) > 1 >= abs(y_distance) or abs(y_distance) > 1 >= abs(x_distance):
        tail_knot.x += 1 * int(x_distance/abs(x_distance)) if x_distance != 0 else 0
        tail_knot.y += 1 * int(y_distance/abs(y_distance)) if y_distance != 0 else 0


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

"""
Same rules but there are 9 knots after the head.

How many positions does the tail of the rope visit at least once?
"""

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
