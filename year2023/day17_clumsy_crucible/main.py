"""
Code adapted from Peter Norvig's notebook:
https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2023.ipynb, accessed 2024-01-15.
"""
import sys
from pathlib import Path
from typing import Optional
from collections import UserDict
from dataclasses import dataclass, field
from typing import Iterator
from heapq import heappop, heappush


Coordinate = tuple[int, int]
Vector = Coordinate


ROW, COLUMN = 0, 1
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    row1, col1 = coord1
    row2, col2 = coord2
    return row1 + row2, col1 + col2


def turn90(direction: Vector, *, right: bool = True) -> Vector:
    """Turn 90 degrees to the right if `right` is True, left otherwise."""
    if direction == RIGHT:
        return DOWN if right else UP
    if direction == LEFT:
        return UP if right else DOWN
    if direction == UP:
        return RIGHT if right else LEFT
    if direction == DOWN:
        return LEFT if right else RIGHT


class Grid(UserDict):
    """A 2D grid implemented as {(row, column): cell}"""
    
    def __init__(self, grid: list[str]):
        self.size = len(grid), max(len(row) for row in grid)
        super().__init__(
            {
                (row, column): int(cell)
                for row, line in enumerate(grid)
                for column, cell in enumerate(line)
            }
        )

    def __missing__(self, nonexistent_coord: Coordinate) -> None:
        return


@dataclass(frozen=True, eq=True)
class State:
    coordinate: Coordinate
    direction: Vector
    steps_consecutive: int


@dataclass(order=True)
class Node:
    heat_loss: int
    state: State = field(compare=False)

    def __iter__(self):
        yield self.heat_loss
        yield self.state


@dataclass
class MinimizeHeatLossProblem:
    city_grid: Grid
    min_consecutive_steps: int = 1
    max_consecutive_steps: int = 3
    start: Coordinate = field(init=False)
    goal: Coordinate = field(init=False)

    def __post_init__(self):
        self.start  = min(self.city_grid)
        self.goal   = max(self.city_grid)
    
    def action_candidates(self, state: State) -> Iterator[Vector]:
        next_directions = []
        if state.steps_consecutive >= self.min_consecutive_steps:
            next_directions.extend(
                [turn90(state.direction), turn90(state.direction, right=False)]
            )
        if state.steps_consecutive < self.max_consecutive_steps:
            next_directions.append(state.direction)
        return (
            direction
            for direction in next_directions
            if add_coordinates(state.coordinate, direction) in self.city_grid
        )
    
    def take_action(self, state: State, next_direction: Vector) -> State:
        same_direction = state.direction == next_direction
        return State(
            add_coordinates(state.coordinate, next_direction),
            next_direction,
            state.steps_consecutive + 1 if same_direction else 1
        )

    def is_goal(self, state: State) -> bool:
        return state.coordinate == self.goal and\
            state.steps_consecutive >= self.min_consecutive_steps
    
    def heat_lost(self, state: State) -> int:
        return self.city_grid[state.coordinate]

    def solve(self) -> Optional[int]:
        """Find the path that minimizes heat loss via Dijkstra's algorithm."""
        to_visit = [
            Node(0, State(self.start, RIGHT, 1)),
            Node(0, State(self.start, DOWN, 1))
        ]
        records: dict[State, int] = {}

        while to_visit:
            heat_loss, current = heappop(to_visit)
            if self.is_goal(current):
                return heat_loss
            for action in self.action_candidates(current):
                next_state = self.take_action(current, action)
                next_heat_loss = self.heat_lost(next_state) + heat_loss
                if next_state not in records or next_heat_loss < records[next_state]:
                    heappush(to_visit, Node(next_heat_loss, next_state))
                    records[next_state] = next_heat_loss
        return None


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    city = Grid(puzzle_input)
    problem = MinimizeHeatLossProblem(city)
    return problem.solve()


def solve_part2(puzzle_input: list[str]) -> int:
    city = Grid(puzzle_input)
    problem = MinimizeHeatLossProblem(
        city, 
        min_consecutive_steps = 4, max_consecutive_steps = 10
    )
    return problem.solve()


if __name__ == '__main__':

    title = 'Day 17: Clumsy crucible'
    print(title.center(50, '-'))


    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The least heat loss the crucible can incur is {part1}.
        Part 2: The least heat loss the crucible can incur is {part2}.
        """)
