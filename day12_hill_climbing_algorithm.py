"""
-- Day 12: Hill Climbing Algorithm --

Usage example:
    Advent_of_Code/year2022 $ python day12_hill_climbing_algorithm.py day12_test.txt day12_input.txt

Inspired by Peter Norvig's solution for a faster part 2, but implemented with BFS instead of A*
"""
import sys
from typing import *
import string
import pathlib
import collections
import itertools
import functools

T = TypeVar('T')

ALPHABETS: Sequence[str] = 'S' + string.ascii_lowercase + 'E'

Coord = collections.namedtuple('Coord', ['row', 'column'])
Vector = Coord
DIRECTIONS4 = Up, Down, Left, Right = \
    tuple(
        map(lambda p: Vector(*p), ((-1, 0), (1, 0), (0, -1), (0, 1)))
    )
DUMMY_OFF_GRID = Coord(-1, -1)    # for part 2


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return Vector(
        *tuple(p + q for p, q in zip(vector1, vector2))
    )


class Grid(dict):
    """Save grid data as a dictionary"""
    def __init__(self, grid: Iterable[T], directions: tuple[Vector], default: T = KeyError) -> None:
        """
        Initialize with a list of characters representing cell values.
        """
        super().__init__()
        self.directions = directions
        self.default = default if default else None
        self.update(
            {
                Coord(row, column): value
                for row, line in enumerate(grid)
                for column, value in enumerate(line)
            }
        )

    def __repr__(self) -> str:
        return '\n'.join(
            ''.join(
                self.get(coord)
                for _, coord in itertools.groupby(row, key=lambda coord: coord.column)
            )
            for _, row in itertools.groupby(self, key=lambda coord: coord.row)
        )

    def __missing__(self, key: Coord):
        if self.default == KeyError:
            raise KeyError(f'Coordinate {key} not in grid')
        else:
            return self.default

    def neighbors(self, coord: Coord) -> list[tuple[Coord, T]]:
        """Get neighboring coordinates of input coord."""
        return [
            (
                neighbor := _add_vectors(coord, d),
                self[neighbor]
            )
            for d in self.directions
            if Coord(coord.row + d.row, coord.column + d.column) in self
        ]


class HillClimbProblem:
    """A class object framing the hill-climbing problem as a path search problem"""

    def __init__(self, grid: Grid, start: Optional[Coord] = None, goal: Optional[Coord] = None, **kwargs):
        self.grid: Grid = grid
        self.start: Coord = start if start else \
            next(coord for coord, val in self.grid.items() if val == ALPHABETS.index('S'))
        self.goal: Coord = goal if goal else\
            next(coord for coord, val in self.grid.items() if val == ALPHABETS.index('E'))
        self.__dict__.update(**kwargs)

    def goal_test(self, state: Coord) -> bool:
        return state == self.goal

    def actions(self, state: Coord) -> list[Coord]:
        return [
            neighbor for neighbor, neighbor_val in self.grid.neighbors(state)
            if neighbor_val - self.grid[state] <= 1
        ]


class HillClimbProblem2(HillClimbProblem):
    """A variation of HillClimbProblem for part 2"""

    def actions(self, state: Coord) -> list[Coord]:
        """
        If state is DUMMY_OFF_GRID, jump to any location with height value 'a'.
        """
        if state == DUMMY_OFF_GRID:
            return [
                p for p, val in self.grid.items() if val == ALPHABETS.index('a')
            ]
        else:
            return [
                neighbor for neighbor, neighbor_val in self.grid.neighbors(state)
                if neighbor_val - self.grid[state] <= 1
            ]


class Node:
    """A node in a search problem"""

    def __init__(self, state: Coord, parent: Optional['Node'] = None, cost: float = 0.0, heuristic: float = 1.0):
        self.state = state
        self.parent = parent
        self.cost, self.heuristic = cost, heuristic  # necessary for A* algorithm

    def __lt__(self, other: 'Node') -> bool:
        """
        Necessary for A* search algorithm when ordering the priority of nodes
        """
        return self.cost + self.heuristic < other.cost + other.heuristic

    def __repr__(self) -> str:
        return f'Node(state={self.state}, parent={self.parent})'


def breadth_first_search(problem: HillClimbProblem, goal_test: Callable[T, bool], successors: Callable[T, T]) -> Optional[Node]:
    """
    Implement breadth-first search algorithm to solve the input problem.
    """
    initial_node: Node = Node(problem.start, parent=None)
    frontier: collections.deque[Node] = collections.deque([initial_node])
    explored: set[T] = set(problem.start)

    while frontier:
        current_node = frontier.popleft()   # pop from left for BFS, pop from right for DFS
        if goal_test(current_node.state):
            frontier.clear()
            explored.clear()
            return current_node
        for child_state in successors(current_node.state):
            if child_state not in explored:
                frontier.append(Node(child_state, parent=current_node))
                explored.add(child_state)
    return None


def trace_path(end_node: Node) -> collections.deque[Coord]:
    """
    Trace the shortest path from the end Node returned by breadth_first_search().
    """
    shortest_path: collections.deque[Coord] = collections.deque([])
    while end_node.parent:
        shortest_path.append(end_node.parent.state)
        end_node = end_node.parent
    shortest_path.reverse()
    if shortest_path[0] == DUMMY_OFF_GRID:
        shortest_path.popleft()
    return shortest_path


def parse(txt_filename: str) -> list[list[int]]:
    """Parse the content of the file by mapping characters to ALPHABETS index."""
    lines: list[str] = pathlib.Path(txt_filename).read_text().split('\n')
    return [
        [ALPHABETS.index(char) for char in line]
        for line in lines
    ]


def _find_path(puzzle_input: list[list[T]], problem_maker: Callable, *args) -> int:
    """
    Instantiate HillClimbProblem object with Grid object instantiated with the data from puzzle_input.
    Find the shortest path with BFS using the default start and end goals.
    """
    grid = Grid(puzzle_input, directions=DIRECTIONS4)
    problem = problem_maker(grid, *args)
    end_node = breadth_first_search(problem, problem.goal_test, problem.actions)
    start_to_goal = trace_path(end_node)

    return len(start_to_goal)


solve_part1 = functools.partial(_find_path, problem_maker=HillClimbProblem)
solve_part2 = functools.partial(
    _find_path,
    problem_maker=functools.partial(HillClimbProblem2, start=DUMMY_OFF_GRID)
)

if __name__ == '__main__':
    title = 'Day 12: Hill Climbing Algorithm'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The shortest path from 'S' to 'E' is {part1} steps.
        Part 2: The shortest path from an 'a' to 'E' is {part2} steps.
        """)
