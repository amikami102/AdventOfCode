"""
-- Day 24: Blizzard Basin --

Usage example
    Advent_Of_code/year2022 $ python day24_blizzard_basin.py day24_test.txt day24_input.txt

The key idea to solving the search problem efficiently is to save the state of the grid only every m minutes
where m is a common multiple of the width and height of the basin (excluding the walls from the length counts).

The code makes two assumptions:
    - None of the blizzard escapes the basin,
    i.e. there are no vertically-flowing blizzards in the columns where the exit and entrance tiles are located.
    - There is a path from the entrance to the exit of the basin and a reverse path too.

The main block of the code contains series of `assert` statements to test the class method and path-search code on a simple example.
"""
import sys
import pathlib
import collections
import math
import queue
import functools
from typing import *

Coord = tuple[int, int]  # (row, column)
Vector = Coord

ROW, COLUMN = 0, 1
ORTHOGONALS = UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
DIRECTIONS = *ORTHOGONALS, (0, 0)   # there is an option to wait
EMPTY, WALL, *BLIZZARDS = '.', '#', '^', 'v', '<', '>'
ARROWS: dict[str, Vector] = {
    '^': UP,
    'v': DOWN,
    '<': LEFT,
    '>': RIGHT
}


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[ROW] + vector2[ROW], vector1[COLUMN] + vector2[COLUMN]


def minmax(iterable: Iterable[int]) -> tuple[int, int]:
    it = list(iterable)
    MinMax = collections.namedtuple('MinMax', ['Min', 'Max'])
    return MinMax(min(it), max(it))


def clock_mod(k: int, m: int) -> int:
    """Equivalent to mod(k, m) except that 0 is replaced by `m`"""
    return (k % m) or m


def slide_mod(coords: Iterable[Coord], delta: Vector, mod: Vector) -> Iterable[Coord]:
    """
    Slide all the points in `coords` by adding `delta` to them but
    return the resulting coordinates corrected by clock_mod.
    """
    (drow, dcol), (mrow, mcol) = delta, mod
    return [
        (clock_mod(row + drow, mrow), clock_mod(col + dcol, mcol))
        for (row, col) in coords
    ]


def manhattan_distance(coord1: Coord, coord2: Coord) -> float:
    """Return the Manhattan distance between `coord1` and `coord2`."""
    return abs(coord1[ROW] - coord2[ROW]) + abs(coord1[COLUMN] - coord2[COLUMN])


class Grid(dict[Coord, str]):
    """A representation of a 2D grid as mapping of coordinates to their cell values"""

    def __init__(self, grid: dict[Coord, str] | list[str], default: str = KeyError,
                 directions: Sequence[Vector] = DIRECTIONS, skip: Sequence[str] = ()):
        super().__init__()
        self.default = default
        self.directions = directions
        self.skip = skip
        if isinstance(grid, dict):
            self.update(grid)
        else:
            self.update(
                {
                    (row, column): value
                    for row, line in enumerate(grid)
                    for column, value in enumerate(line)
                    if value not in self.skip
                }
            )

    def __missing__(self, key: Coord) -> str:
        if self.default is KeyError:
            raise KeyError(f'{key} not found in this grid')
        else:
            return self.default

    def get_neighbors(self, key: Coord, cell_value: bool = False) -> Iterator[Coord | str]:
        if cell_value:
            return (
                self[_add_vectors(key, direction)] for direction in self.directions
            )
        else:
            return (
                _add_vectors(key, direction) for direction in self.directions
            )

    def __repr__(self) -> str:
        """
        Return the grid as string,
        filling in missing coordinates with empty string or self.default.
        """
        r0, r1 = minmax(coord[ROW] for coord in self.keys())
        c0, c1 = minmax(coord[COLUMN] for coord in self.keys())
        placeholder = '' if self.default is KeyError else self.default
        return '\n'.join(
            ''.join(
                self.get((row, column), placeholder) for column in range(c0, c1 + 1)
            )
            for row in range(r0, r1 + 1)
        )


class BasinState(NamedTuple):
    """
    A namedtuple to store the state of the agent, where they are (`loc`) at what time (`time`)
    """
    time: Optional[int]
    loc: Coord

    def __repr__(self) -> str:
        return f'BasinState(time={self.time}, loc={self.loc})'


class Node:
    """
    A wrapper around BasinState that keeps track of how we got from one BasinState to the next
    """

    def __init__(self, state: BasinState,
                 parent: 'Node' = None, cost: float = 0.0, heuristic: float = 1.0) -> None:
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self) -> str:
        return f'Node(state={self.state}, cost={self.cost})'

    def __lt__(self, other: 'Node') -> bool:
        """Necessary for sorting nodes in a priority queue"""
        return self.cost + self.heuristic < other.cost + other.heuristic


class BasinProblem:
    """A class object representing the search problem"""

    def __init__(self, grid: Grid) -> None:
        """
        Set up the problem and cache the empty ground locations for all future times.

        The initial state is the upper-left most tile that is EMPTY at time 0.
        The goal is located at the lower-right most tile that is EMPTY.

        The largest vertical distance a blizzard can move over is maximum row coordinate of a non-WALL cell (which is occupied by exit tile) - 1.
        The largest horizontal distance a blizzard can move over is maximum column coordinate of a non-WALL cell.
        """
        self.grid = grid
        self.height, self.width = \
            max(coord[ROW] for coord, value in self.grid.items()) - 1, \
            max(coord[COLUMN] for coord, value in self.grid.items()) - 1

        initial_empties = {
            coord for coord, value in self.grid.items() if value == EMPTY
        }
        self.initial: BasinState = BasinState(time=0, loc=min(initial_empties))
        self.goal: BasinState = BasinState(time=None, loc=max(initial_empties))

        self.empties: dict[int, set[Coord]] = collections.defaultdict(set)
        self.cache_empties()

    def __repr__(self) -> str:
        return f'BasinProblem looking for the shortest path from {self.initial} to {self.goal.loc}'

    def cache_empties(self) -> None:
        """
        Store in `self.empties[t]` all the coordinates that are empty of blizzards
        at time t for t between 0 and `m`, the least common multiple of basin shape parameters.
        """
        basin_coords: set[Coord] = {
            coord for coord, value in self.grid.items() if value != WALL
        }
        blizzards: dict[str, set[Coord]] = {
            arrow: {coord for coord in basin_coords if self.grid[coord] == arrow}
            for arrow in BLIZZARDS
        }
        m: int = math.lcm(self.width, self.height)

        for t in range(m):
            self.empties[t] = basin_coords - set().union(*blizzards.values())
            blizzards = {
                arrow: set(slide_mod(blizzards[arrow], delta, (self.height, self.width)))
                for arrow, delta in ARROWS.items()
            }

    def actions(self, state: BasinState) -> Iterator[BasinState]:
        """
        Generate the next possible actions from `state`,
        which are BasinState at next increment of time and one of the EMPTY tile neighbors of `state.loc`.
        """
        m: int = math.lcm(self.width, self.height)
        t2: int = (state.time + 1) % m
        yield from (
            BasinState(time=t2, loc=coord)
            for coord in self.grid.get_neighbors(state.loc)
            if coord in self.empties[t2]
        )

    def heuristic(self, state: BasinState) -> float:
        return manhattan_distance(state.loc, self.goal.loc)


def goal_test(problem: BasinProblem, node: Node) -> bool:
    return node.state.loc == problem.goal.loc


def successors(problem: BasinProblem, node: Node) -> Iterator[Node]:
    """Generate children nodes from `node`"""
    for action in problem.actions(node.state):
        yield Node(
            state=action,
            parent=node,
            cost=node.cost + 1.0,
            heuristic=problem.heuristic(action)
        )


def a_star_search(
        problem: BasinProblem,
        goal_test: Callable[[BasinProblem, Node], bool],
        successors: Callable[[BasinProblem, Node], Iterator[Node]]
    ) -> Node:
    """
    Implement A* algorithm that searches the lowest f(node) value first.
    """
    frontier: queue.PriorityQueue[Node] = queue.PriorityQueue()
    explored: dict[BasinState, Node] = {}

    initial_node: Node = Node(state=problem.initial)
    frontier.put(initial_node)
    explored[initial_node.state] = initial_node

    while frontier:
        current_node: Node = frontier.get()

        if goal_test(problem, current_node):
            return current_node

        for child_node in successors(problem, current_node):
            child_state = child_node.state
            if child_state not in explored \
                    or child_node.cost < explored[child_state].cost:
                frontier.put(child_node)
                explored[child_state] = child_node
    raise Exception('Never found a path')


def reverse_trip(problem: BasinProblem, offset: int) -> BasinProblem:
    """
    Reverse the initial and goal locations of `problem`.
    Pad the `time` attribute of initial by `offset`.
    Return the mutated `problem`, not a new instance of BasinProblem.
    """
    initial, goal = problem.initial, problem.goal
    problem.initial = BasinState(time=initial.time + offset, loc=goal.loc)
    problem.goal = BasinState(time=None, loc=initial.loc)
    return problem


solve = functools.partial(a_star_search, goal_test=goal_test, successors=successors)


def parse(txt_filename: str) -> list[str]:
    """Return the content of the file as list of strings"""
    return pathlib.Path(txt_filename).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    """Return the fewest number of minutes required to exit the basin"""
    grid = Grid(puzzle_input)
    problem = BasinProblem(grid)
    return int(solve(problem).cost)


def solve_part2(puzzle_input: list[str]) -> int:
    """
    Make a three-leg trip where
        leg 1 is from basin entrance to the exit,
        leg 2 is the reverse of leg 1, and
        leg 3 is a repeat of leg 1.
    Return the number of minutes it takes to complete the whole trip.
    """
    grid = Grid(puzzle_input)
    problem = BasinProblem(grid)

    leg1 = solve(problem)
    leg2 = solve(reverse_trip(problem, leg1.cost))
    leg3 = solve(reverse_trip(problem, leg2.cost))
    return int(leg1.cost + leg2.cost + leg3.cost)


if __name__ == '__main__':
    title = 'Day 24: Blizzard Basin'
    print(title.center(50, '-'))

    # test clock_mod() works
    assert clock_mod(0, 12) == 12
    assert clock_mod(1, 12) == 1 % 12
    assert clock_mod(10, 12) == 10
    assert clock_mod(23, 12) == 23 % 12
    assert clock_mod(24, 12) == 12

    # test that slide_mod() works
    # by sliding blizzards at (1,1), (2,2), (3,3), (4,4) within a basin shaped 5 rows by 4 columns
    # n.b. This basin is completely enclosed by walls, no exit or entrance.
    testBlizzards = [(1, 1), (2, 2), (3, 3), (4, 4)]
    testShape = 5, 4  # number of rows, number of columns
    assert slide_mod(testBlizzards, RIGHT, testShape) == [(1, 2), (2, 3), (3, 4), (4, 1)]
    assert slide_mod(testBlizzards, LEFT, testShape) == [(1, 4), (2, 1), (3, 2), (4, 3)]
    assert slide_mod(testBlizzards, UP, testShape) == [(5, 1), (1, 2), (2, 3), (3, 4)]
    assert slide_mod(testBlizzards, DOWN, testShape) == [(2, 1), (3, 2), (4, 3), (5, 4)]
    assert slide_mod(testBlizzards, (0, 4), testShape) == testBlizzards

    # test that manhattan_distance() works correctly
    target = (6, 5)
    assert manhattan_distance((0, 0), target) == abs(6) + abs(5)
    assert manhattan_distance((14, 11), target) == abs(14 - 6) + abs(11 - 5)

    # test that BasinProblem initializes correctly and its methods work
    test = [
        '#.#####',
        '#.....#',
        '#>....#',
        '#.....#',
        '#...v.#',
        '#.....#',
        '#####.#'
    ]
    testProblem = BasinProblem(Grid(test))
    assert testProblem.initial.loc == (0, 1)
    assert testProblem.goal.loc == (6, 5)
    assert testProblem.width == 5 and testProblem.height == 5

    # test that BasinProblem.cache_empties() works
    assert len(testProblem.empties) == math.lcm(testProblem.width, testProblem.height)
    empties_at_time0 = {
        coord for coord, value in testProblem.grid.items()
        if value == EMPTY
    }
    empties_at_time1 = empties_at_time0 - {(2, 2), (5, 4)} | {(2, 1), (4, 4)}
    empties_at_time2 = empties_at_time0 - {(2, 3), (1, 4)} | {(2, 1), (4, 4)}
    empties_at_time3 = empties_at_time0 - {(2, 4)} | {(2, 1), (4, 4)}
    empties_at_time4 = empties_at_time0 - {(2, 5), (3, 4)} | {(2, 1), (4, 4)}
    assert testProblem.empties[0] == empties_at_time0
    assert testProblem.empties[1] == empties_at_time1
    assert testProblem.empties[2] == empties_at_time2
    assert testProblem.empties[3] == empties_at_time3
    assert testProblem.empties[4] == empties_at_time4

    # test that BasinProblem.actions() works
    state_at_time1 = BasinState(time=1, loc=(1, 1))
    possible_actions_at_time1 = {
        BasinState(time=2, loc=_add_vectors(state_at_time1.loc, UP)),
        BasinState(time=2, loc=_add_vectors(state_at_time1.loc, RIGHT)),
        BasinState(time=2, loc=_add_vectors(state_at_time1.loc, DOWN)),
        BasinState(time=2, loc=state_at_time1.loc)  # don't move
    }
    assert set(testProblem.actions(state_at_time1)) == possible_actions_at_time1

    # test that BasinProblem.heuristic() works
    assert testProblem.heuristic(state_at_time1) == manhattan_distance(state_at_time1.loc, testProblem.goal.loc)

    # test that goal_test() works
    testNode = Node(
        state=state_at_time1,
        parent=Node(testProblem.initial),
        cost=1,
        heuristic=testProblem.heuristic(state_at_time1)
    )
    assert not goal_test(testProblem, testNode)
    fakeFinalNode = Node(state=BasinState(loc=(6, 5), time=None))
    assert goal_test(testProblem, fakeFinalNode)

    # test that successors() works
    assert {child.state for child in successors(testProblem, testNode)} == possible_actions_at_time1

    # test that a_star_search() works
    assert a_star_search(testProblem, goal_test, successors)

    # test that reverse_trip() works
    testSolution: Node = solve(testProblem)
    testReverseProblem: BasinProblem = reverse_trip(
        testProblem,
        testSolution.cost if testSolution else 0
    )
    assert testReverseProblem.goal.loc == (0, 1)
    assert testReverseProblem.initial.time == 0 + testSolution.cost
    testNextInitialTime: int = testReverseProblem.initial.time
    testReverseSolution: Node = solve(testReverseProblem)
    testReReverseProblem: BasinProblem = reverse_trip(
        testReverseProblem,
        testReverseSolution.cost if testReverseSolution else 0
    )
    assert testReReverseProblem.goal.loc == (6, 5)
    assert testReReverseProblem.initial.time == testNextInitialTime + testReverseSolution.cost

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{file}:
        Part 1: The fewest number of minutes to reach the goal avoiding the blizzards is {part1}.
        Part 2: The shortest time to reach the goal, go back to the start, then reach the goal again is {part2}.
        """)
