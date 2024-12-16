"""
The key to Part 2 is that Python's dictionary is sorted by insertion order.
My code uses `collections.OrderedDict` to explicitly use the sortability.
"""
import sys
from pathlib import Path
from collections import OrderedDict


Box = OrderedDict[str, int]


DASH = '-'
EQUALS = '='
N_BOXES = 256


def hash_holiday_ascii(string: str) -> int:
    """Convert `string` to an integer according to holiday ASCII algorithm."""
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current = current % 256
    return current


def execute_initialization_sequence(steps: list[str]) -> list[Box]:
    boxes = [OrderedDict() for _ in range(N_BOXES)]
    for step in steps:
        label, symbol, focus = step.partition(
            DASH if DASH in step else EQUALS
        )
        box = boxes[hash_holiday_ascii(label)]
        if symbol == DASH:
            if label in box:
                box.pop(label)
        else:
            box[label] = int(focus)
    return boxes


def add_focusing_powers(boxes: list[Box]) -> int:
    return sum(
        box * slot * slots[label]
        for box, slots in enumerate(boxes, start=1)
        for slot, label in enumerate(slots, start=1)
    )


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().split(',')


def solve_part1(puzzle_input: list[str]) -> int:
    return sum(
        hash_holiday_ascii(step)
        for step in puzzle_input
    )


def solve_part2(puzzle_input) -> int:
    boxes_filled = execute_initialization_sequence(puzzle_input)
    return add_focusing_powers(boxes_filled)


if __name__ == '__main__':

    title = 'Day 15: Lens library'
    print(title.center(50, '-'))

    assert hash_holiday_ascii('HASH') == 52
    assert hash_holiday_ascii('rn') == 0
    assert hash_holiday_ascii('qp') == 1

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The sum of the initialization sequence is {part1}.
        Part 2: The sum of the focusing powers is {part2}.
        """)
