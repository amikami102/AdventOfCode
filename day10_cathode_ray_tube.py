"""
addx V
    takes two cycles to complete. After two cycles, the X register is increased by the value V.
    (V can be negative.)
noop
    takes one cycle to complete. It has no other effect.

Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
What is the sum of these six signal strengths?
---
Cycle, start X, end X, executing
1, 1, 1, noop
2, 1, 1, addx
3, 1, 1 + 3 = 4, addx
4, 4, 4, addx -5
5, 4, 4 + (-5) = -1, addx
"""
from pprint import pprint
import re
import itertools

addx_pattern = re.compile(r"^addx (?P<value>-?\d+)$")

cycles = []
with open('day10_input.txt', 'r') as f:
    c, X = 0, 1
    for line in f:
        matched = re.match(addx_pattern, line.strip())
        if matched is None:
            c += 1
            cycles.append((X, X))
        else:
            cycles.append((X, X))
            end = X + int(matched.group('value'))
            cycles.append((X, end))
            X = end

total_strength = 0
for i, cycle in enumerate(cycles):
    if i+1 in [20, 60, 100, 140, 180, 220]:
        print(cycle)
        total_strength += (i+1) * cycle[0]
pprint(total_strength)

"""
Part 2
"""


def draw_pixel(position: int, X: int) -> str:
    """
    Draw '#' if the sprite covers the pixel position of current cycle
    and '.' otherwise.
    """
    sprite = {X-1, X, X + 1}
    width = 40
    return '#' if position % width in sprite else '.'


pixels = []
for i, cycle in enumerate(cycles):
    X_start, X_end = cycle
    pixel = draw_pixel(i, X_start)
    pixels.append(pixel)

width = 40
lines = [iter(pixels)] * width
for line in zip(*lines):
    print(''.join(itertools.chain(*line)))