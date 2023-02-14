"""
-- Day 24: Blizzard Basin --
"""
from typing import *
import collections
import queue
import math
from heapq import heappush, heappop

T = TypeVar('T')  # arbitrary type
Point = collections.namedtuple('Point', ['x', 'y'])
Vector = Point
orthogonals = North, South, West, East = (-1, 0), (1, 0), (0, -1), (0, 1)
wait = (0, 0)
EMPTY: str = '.'
WALL: str = '#'
BLIZZARDS: dict[str, Vector] = {
    '^': North, 'v': South, '>': East, '<': West
}


def minmax(iterator: Iterator[int]) -> tuple[int, int]:
    """Return the minimum and maximum of input interator"""
    it = list(iterator)
    MinMax = collections.namedtuple('MinMax', ['Min', 'Max'])
    return MinMax(min(it), max(it))


class Grid(collections.defaultdict):
    """ A 2d grid represented as a mapping of {(x, y): cell_value} """

    def __init__(self, grid: list[str], default: str = None, directions: Iterable[tuple[int, int]] = orthogonals):
        """Initialize with Grid(['...###.', '...####']) """
        super().__init__()
        self.default = default
        self.directions = directions
        self.update(
            {
                Point(x, y): value
                for x, line in enumerate(grid)
                for y, value in enumerate(line)
            }
        )

    def __missing__(self, key):
        if self.default is None:
            raise IndexError('Out of grid bounds')
        else:
            return self.default

    def get_neighbors(self, point: Point) -> Iterator[Point]:
        return (
            Point(point.x + dx, point.y + dy)
            for (dx, dy) in self.directions
        )

    def size(self) -> tuple[int, int]:
        """Return the horizontal and vertical lengths of the grid"""
        xmin, xmax = minmax(point.x for point in self.keys())
        ymin, ymax = minmax(point.y for point in self.keys())
        return (xmax - xmin) + 1, (ymax - ymin) + 1


# Node = collections.namedtuple('Node', ['state', 'parent', 'cost', 'heuristic'])
BasinState = collections.namedtuple('BasinState', ['point', 't'])


class Node:
    def __init__(self,
                 state: BasinState, parent: 'Node' = None, cost: float = 0.0, heuristic: float = 1.0) -> None:
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self) -> str:
        return f'Node(state={self.state}, cost={self.cost})'

    def __lt__(self, other: 'Node') -> bool:
        # Necessary for adding nodes to priority queue
        return self.cost + self.heuristic < other.cost + other.heuristic


class BasinProblem:
    """Frame the problem as search problem"""

    def __init__(self, grid: Grid) -> None:
        empties = {point for point, value in grid.items() if value == EMPTY}
        self.initial: BasinState = BasinState(t=0, point=min(empties))
        self.goal: BasinState = BasinState(t=None, point=max(empties))
        self.grid: Grid = grid
        self.empties: dict[int, list[Point]] = collections.defaultdict(list)
        self.cache_empties()

    def is_goal(self, current_state: BasinState) -> bool:
        return current_state.point == self.goal.point

    def heuristic(self, current_state: BasinState) -> float:
        # return manhattan distance to the goal.point
        x0, y0 = current_state.point
        x1, y1 = self.goal.point
        return abs(x0 - x1) + abs(y0 - y1)

    def cache_empties(self) -> None:
        """
        Every least-common-multiple minutes, the blizzards return to their original positions.
        Thus, the states we want to cache are the state of basin during the least-common-multiple period.
        """
        basin: set[Point] = set()
        blizzards: dict[str, set[Point]] = collections.defaultdict(set)
        clock_mod: Callable[tuple[int, int], int] = lambda i, m: (i % m) or m

        def slide_points(points: Iterable[Point], dx: int, dy: int, mx: int, my: int) -> Iterable[Point]:
            """
            Using clock-mod instead of regular mod because the grid's x=0 and y=0 are the walls.
            """
            return {
                Point(clock_mod(x + dx, mx), clock_mod(y + dy, my))
                for x, y in points
            }

        nrows, ncols = self.grid.size()[0] - 2, self.grid.size()[1] - 2
        least_common_multiple = math.lcm(nrows, ncols)

        for point, value in self.grid.items():
            if value in BLIZZARDS.keys():
                blizzards[value].add(point)
            if value != WALL:
                basin.add(point)
        for t in range(least_common_multiple):
            self.empties[t] = sorted(list(basin.difference(set().union(*blizzards.values()))))
            blizzards = {
                arrow: slide_points(blizzards[arrow], *BLIZZARDS[arrow], nrows, ncols)
                for arrow in BLIZZARDS.keys()
            }


def successors(problem: BasinProblem, parent_node: Node) -> Iterable[Node]:
    parent_state = parent_node.state
    t2 = (parent_state.t + 1) % len(problem.empties)
    actions = [
        BasinState(t=t2, point=point)
        for point in problem.grid.get_neighbors(parent_state.point)
        if point in problem.empties[t2] or point == problem.goal.point
    ]
    return [
        Node(
            state=action_state,
            parent=parent_node,
            cost=parent_node.cost + 1.0,
            heuristic=problem.heuristic(parent_state)
        )
        for action_state in actions
    ]


with open('day24_input.txt', 'r') as f:
    basin_problem = BasinProblem(
        grid=Grid(
            f.read().splitlines(),
            directions=(*orthogonals, wait)
        )
    )


def a_star_search(problem: BasinProblem) -> Optional[Node]:
    """
    Implement an A* algorithm to navigate through the basin with the shortest path.
    Return the final node if the final node reaches the goal state or None if there is no solution.
    """
    initial_node = Node(problem.initial)
    frontier: queue.PriorityQueue = queue.PriorityQueue()
    frontier.put(initial_node)
    explored: dict[BasinState, float] = {}
    explored.update({problem.initial: 0.0})

    while frontier:
        cur_node: Node = frontier.get()
        cur_state: BasinState = cur_node.state
        if problem.is_goal(cur_state):
            return cur_node
        for child_node in successors(problem, cur_node):
            child_state = child_node.state
            if child_state not in explored or explored[child_state] > child_node.cost:
                frontier.put(child_node)
                explored[child_state] = child_node.cost
    return None


part1 = a_star_search(basin_problem)
print(f'Part 1: {int(part1.cost)} minutes')