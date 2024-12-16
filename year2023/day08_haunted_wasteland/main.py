import sys
from typing import Iterator
from pathlib import Path
import re
from itertools import cycle
import math
from functools import reduce


Network = dict[str, tuple[str, str]]


def extract_nodes(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r'[1-9A-Z]+', text))


def parse(filename: str) -> tuple[str]:
    return tuple(
        line.strip()
        for line in Path(filename).read_text().splitlines()
        if line.strip()
    )


def convert_direction(direction: str) -> list[int]:
    return [0 if letter == 'L' else 1 for letter in direction]


def parse_nodes(node_lines: list[str]) -> Network:
    iterator = (extract_nodes(line) for line in node_lines)
    return {
        node: (left, right)
        for node, left, right in iterator
    }
    

def navigate(
        directions: list[int], network: Network, node: str = 'AAA', goal: str = 'ZZZ'
    ) -> Iterator[str]:
    instructions = cycle(directions)
    while not node.endswith(goal):
        node = network[node][next(instructions)]
        yield node
    

def solve_part1(puzzle_input) -> int:
    lr_sequence, *nodes = puzzle_input
    directions = convert_direction(lr_sequence)
    network = parse_nodes(nodes)
    return sum(
        1 for _ in navigate(directions, network)
    )


def solve_part2(puzzle_input) -> int:
    lr_sequence, *nodes = puzzle_input
    directions = convert_direction(lr_sequence)
    network = parse_nodes(nodes)
    steps_to_reach_Z = [
        (node, sum(1 for _ in navigate(directions, network, node, 'Z')))
        for node in network
        if node.endswith('A')
    ]
    return reduce(math.lcm, (steps for _, steps in steps_to_reach_Z))
    

if __name__ == '__main__':
    title = 'Day 08: Haunted wasteland'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1, part2 = None, None
        if txtfile != 'test3.txt':
            part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The number of steps to get from AAA to ZZZ is {part1}.
        Part 2: The number of steps to simultaneously reach the 'Z' nodes is {part2}.
        """)
