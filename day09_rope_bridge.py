"""
Simulate your complete hypothetical series of motions.
How many positions does the tail of the rope visit at least once?
"""
from pprint import pprint
import collections


class knot:
    def __init__(self, label):
        self.x, self.y = 0, 0
        self.label = label
        self.history = []

    def is_touching(self, other) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def write_history(self):
        self.history.append((self.x, self.y))


head, tail = knot('head'), knot('tail')

def update_tail_coord(*head_coord) -> None:
    x, y = head_coord
    x_distance = x - tail.x
    y_distance = y - tail.y

    if abs(x_distance) <= 1 and abs(y_distance) <= 1:
        tail.x += 0
        tail.y += 0
    elif abs(x_distance) > 1 and abs(y_distance) > 1:
        raise ValueError('Head moved too fast')
    elif abs(x_distance) > 1 >= abs(y_distance) or abs(y_distance) > 1 >= abs(x_distance):
        tail.x += 1 * int(x_distance/abs(x_distance)) if x_distance != 0 else 0
        tail.y += 1 * int(y_distance/abs(y_distance)) if y_distance != 0 else 0


with open('day09_input.txt', 'r') as f:
    head.history.append((head.x, head.y))
    for line in f:
        direction, steps = line.strip().split(' ')[0], int(line.strip().split(' ')[1])
        for i in range(steps):
            if direction == 'R':
                head.x += 1
            elif direction == 'L':
                head.x -= 1
            elif direction == 'U':
                head.y += 1
            else:
                head.y -= 1
            head.write_history()


for coord in head.history:
    update_tail_coord(*coord)
    tail.write_history()

for knots in zip(head.history, tail.history):
    pprint(knots)

pprint(len(set(tail.history)))

"""
"""