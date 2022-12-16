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
import collections

addx_pattern = re.compile(r"^addx (?P<value>-?\d+)$")
cycle = collections.namedtuple('cycle', ['c', 'start', 'end', 'executing'])

signals = []
with open('day10_input.txt', 'r') as f:
    c, X = 0, 1
    for line in f:
        matched = re.match(addx_pattern, line.strip())
        if matched is None:
            c += 1
            signals.append(cycle(c, X, X, line.strip()))
        else:
            c += 1
            signals.append(cycle(c, X, X, line.strip()))
            c += 1
            end = X + int(matched.group('value'))
            signals.append(cycle(c, X, end, line.strip()))
            X = end


total_strength = 0
for cycle in signals:
    if cycle.c in [20, 60, 100, 140, 180, 220]:
        print(cycle)
        total_strength += cycle.c * cycle.start
pprint(total_strength)
