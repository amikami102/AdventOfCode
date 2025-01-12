# year2024/day15/main.py
import sys
from pathlib import Path 
from typing import Iterable
from itertools import takewhile
from collections import deque

from Grid import *

ARROW_MAP = {
    '^': NORTH, 'v': SOUTH, '<': WEST, '>': EAST
}
EMPTY = '.'
WALL = '#'
OBOX, LBOX, RBOX = 'O', '[', ']'
ROBOT = '@'


def parse(txtfile) -> list[list[str]]:
    return Path(txtfile).read_text().split('\n\n')


class Warehouse(Grid):
    """For part 1"""
    def __init__(self, data: str):
        super().__init__(data.splitlines(), default=None, skip=EMPTY)
        self.boxes = {OBOX}
    
    def locate_robot(self) -> Coordinate:
        locations = self.find_cells(ROBOT)
        if len(locations) > 1:
            raise ValueError(
                f'multiple robots in this warehouse: {locations}'
            )
        return next(iter(locations))
    
    def has_movable_item(self, here: Coordinate) -> bool:
        return self[here] in self.boxes | {ROBOT}

    def get_movable_items(self, 
            direction: Vector, 
            start: Coordinate = None
        ) -> Iterable[Coordinate]:
        if not start:
            start = self.locate_robot()
        return takewhile(
            self.has_movable_item, self.down_the_line(start, direction)
        )

    def shift_items(self, 
            direction: Vector, 
            start: Coordinate = None
        ) -> None:
        movables = deque(self.get_movable_items(direction, start))
        while movables:
            old_location = movables.pop()
            new_location = add_coordinates(old_location, direction)
            if not self[new_location]:
                self[new_location] = self[old_location]
                self.pop(old_location)
    
    def get_total_gps(self) -> int:
        return sum(
            box[ROW] * 100 + box[COLUMN]
            for box in self.find_cells(self.boxes)
            if self[box] == OBOX or self[box] == LBOX
        )


class DoubleWarehouse(Warehouse):
    """For part 2"""
    def __init__(self, data: list[str]):
        super().__init__(data)
        self.boxes = {LBOX, RBOX}
    
    @staticmethod
    def double(raw: str) -> 'DoubleWarehouse':
        return DoubleWarehouse(
            raw
            .replace(WALL, WALL*2)
            .replace(OBOX, LBOX + RBOX)
            .replace(EMPTY, EMPTY * 2)
            .replace(ROBOT, ROBOT + EMPTY)
        )
    
    def get_movable_items(
            self, 
            direction: Vector,
            start: Coordinate = None
        ) -> Iterable[Coordinate]:
        if not start:
            start = self.locate_robot()
        if direction in {EAST, WEST}:
            return set(super().get_movable_items(direction, start=start))
        else: 
            items = {start}
            ahead = add_coordinates(start, direction)
            if self.has_movable_item(ahead):
                items |= set(self.get_movable_items(direction, ahead))
            if self[ahead] == LBOX:
                other_side = add_coordinates(ahead, EAST)
                items |= set(self.get_movable_items(direction, other_side))
            if self[ahead] == RBOX:
                other_side = add_coordinates(ahead, WEST)
                items |= set(self.get_movable_items(direction, other_side))
            return items
    
    def shift_items(
            self,
            direction: Vector
        ) -> None:
        movables = self.get_movable_items(direction)
        any_blocked_by_wall = any(
            self[add_coordinates(item_location, direction)] == WALL
            for item_location in movables
        )
        if not any_blocked_by_wall:
            new_layout = {
                add_coordinates(old, direction): self[old]
                for old in movables
            }
            for old in movables:
                self.pop(old)
            self.update(new_layout)


def robot_walk(warehouse: Warehouse, arrows: str) -> Warehouse:
    """
    Walk the robot in `warehouse` according to the direction in `arrows`.
    Return the final warehouse layout.
    """
    for arrow in arrows:
        warehouse.shift_items(ARROW_MAP[arrow])
    return warehouse


def solve_part1(data) -> int:
    item1, item2 = data 
    warehouse = Warehouse(item1)
    moves = ''.join(item2.splitlines())
    robot_walk(warehouse, moves)
    return warehouse.get_total_gps()


def solve_part2(data):
    item1, item2 = data 
    warehouse = DoubleWarehouse.double(item1)
    moves = ''.join(item2.splitlines())
    robot_walk(warehouse, moves)
    return warehouse.get_total_gps()


if __name__ == '__main__':
    title = 'Day 15: Warehouse Woes'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The total GPS is {part1}.
        Part 2: The total GPS is {part2}.
        """)