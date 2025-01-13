# year2024/day16/main.py
import sys
from pathlib import Path 
from typing import Optional, Iterable, Iterator, Any, Literal, Type, Sequence
from numbers import Number
from dataclasses import dataclass, field
from heapq import heappush, heappop

from Grid import *

Action = Type[Literal[CLOCKWISE, COUNTERCLOCKWISE] | Vector]
WALL = '#'
EMPTY = '.'
START = 'S'
END = 'E'
STEP_COST, TURN_COST = 1, 1000

@dataclass(frozen=True)
class State:
    coordinate: Coordinate
    facing: Vector 

    def __iter__(self):
        yield from (self.coordinate, self.facing)


@dataclass 
class Node:
    state: State 
    parent: Optional['Node']
    cost: Number


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)

    def __iter__(self):
        yield from (self.priority, self.item)


@dataclass
class ReindeerMaze:
    grid: Grid
    start: Coordinate = field(init=False)
    goal: Coordinate = field(init=False)
    initial: Node = field(init=False)

    def __post_init__(self):
        self.goal = next(iter(self.grid.find_cells(END)))
        self.start = next(iter(self.grid.find_cells(START)))
        self.initial: Node = Node(State(self.start, EAST), None, 0)
    
    def reached_goal(self, state: State) -> bool:
        return state.coordinate == self.goal

    def action_cost(self, action: Action) -> Number:
        return TURN_COST if action in {CLOCKWISE, COUNTERCLOCKWISE} else STEP_COST

    def heuristic(self, node: Node) -> Number:
        return manhattan_distance(node.state.coordinate, self.goal)
    
    def generate_actions(self, state: State) -> Iterator[Action]:
        """
        Generate the possible actions from `state`.
        If moving forward from `state` is blocked by a wall, yield only turn options.
        Otherwise, yield turns and forward move.
        """
        forward = add_coordinates(state.coordinate, state.facing)
        if self.grid[forward] == WALL:
            yield from (CLOCKWISE, COUNTERCLOCKWISE)
        else:
            yield from (CLOCKWISE, COUNTERCLOCKWISE, state.facing)
    
    def take_action(self, state: State, action: Action) -> State:
        """
        If `action` is clockwise or counter-clockwise turn, 
        return a state in the same coordinate as `state` but turned cw or ccw.
        Otherwise, return a state that has moved forward.
        """
        if action in {CLOCKWISE, COUNTERCLOCKWISE}:
            return State(state.coordinate, rotate(state.facing, action))
        else:
            return State(add_coordinates(state.coordinate, state.facing), state.facing)
    
    def get_priority_order(self, node: Node) -> PrioritizedItem:
        return PrioritizedItem(
            node.cost + self.heuristic(node),
            node
        )
    
    def display_path(self, node: Node) -> None:
        arrow_map: dict[Vector, str] = {
            direction: arrow 
            for arrow, direction in ARROW_MAP.items()
        }
        for (coordinate, facing) in node_to_path(node):
            if not coordinate in {self.start, self.goal}:
                self.grid[coordinate] = arrow_map[facing]
        self.grid.display_grid(fill=EMPTY)
    
    
def node_to_path(node: Node) -> Sequence[State]:
    """
    Return the path encapsulated in `node` as a sequence of States.
    """
    if not node:
        return []
    else:
        return node_to_path(node.parent) + [node.state]
    

def get_all_best_positions(best_path_nodes: Iterable[Node]) -> set[State]:
    """
    Return a set of coordinates in the maze that are on 
    at least one of the paths in `best_paths`.
    """
    return {
        state.coordinate 
        for node in best_path_nodes
        for state in node_to_path(node)
    }
        

def a_star_search_all(maze: ReindeerMaze) -> Iterable[Node]:
    """Returns all paths through `maze` that have the same cost."""
    frontier: list[PrioritizedItem] = []
    heappush(frontier, maze.get_priority_order(maze.initial))
    explored: dict[State, Node] = {maze.initial.state: maze.initial}

    while frontier:
        _, current = heappop(frontier)
        if maze.reached_goal(current.state):
            return [current] + [
                node
                for priority, node in frontier 
                if priority == current.cost and maze.reached_goal(node.state)
            ]
        for next_action in maze.generate_actions(current.state):
            next_state = maze.take_action(current.state, next_action)
            next_cost = current.cost + maze.action_cost(next_action)
            next_node = Node(next_state, current, next_cost)
            if next_state not in explored or next_cost <= explored[next_state].cost:
                explored[next_state] = next_node 
                heappush(frontier, maze.get_priority_order(next_node))
    return []


def parse(txtfile):
    return Path(txtfile).read_text().splitlines()


def solve_part1(data) -> int:
    maze = ReindeerMaze(Grid(data))
    cheapest_path: Node = next(iter(a_star_search_all(maze)))
    maze.display_path(cheapest_path)
    return cheapest_path.cost 


def solve_part2(data):
    maze = ReindeerMaze(Grid(data))
    cheapest_paths = list(a_star_search_all(maze))
    # for path in cheapest_paths:
    #     maze.display_path(path)
    return len(get_all_best_positions(cheapest_paths))


if __name__ == '__main__':
    title = 'Day 16: Reindeer Maze'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The lowest possible score is {part1}.
        Part 2: The number of tiles in at least one of the best possible paths is {part2}.
        """)