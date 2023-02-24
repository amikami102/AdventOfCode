"""
-- Day 16: Proboscidea Volcanium --

Inspired by
    - https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day16.py
    - https://github.com/mebeim/aoc/blob/8b5f3ef09cb6ddd98a99f8139dd3007ffa3e3d36/2022/solutions/day16.py


Part 1:
The keys to solving efficiently are
    1) only open valves with non-zero flow rates and
    2) use Floyd-Warshall algorithm to measure the distance between any two valves.

_depth_first_search() uses integers to represent which set of valves are open.
    - The ith valve with non-zero flow rate is represented by 1 >> i, or equivalently 2^i.
    - Integer value 0 represents the state where none of the valves are open.
    - Let p represent the sets of valves opened.
    - Valve i is open if p & 2^i equals 1 and closed otherwise.
    - Valve i is added to p by taking the union, p | 2^i.

"""
import sys
import pathlib
import re
import math
import collections
import itertools

Valve = collections.namedtuple('Valve', ['name', 'flow_rate', 'connections'])
Nodes = dict[str, tuple[int, int]]
Edges = dict[str, dict[str, int]]

VALVE_PATTERN = re.compile(
    r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnel[s]* lead[s]* to valve[s]* (.*)'
)


def parse(txt_filename: str) -> list[Valve]:
    """
    Parse each line in the txt_filename and write the data as Valve class object.
    """
    return [
        Valve(*VALVE_PATTERN.match(line).groups())
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


def _floyd_warshall(valves: list[Valve]) -> Edges:
    """
    Return a dictionary of all pairs of valves and their shortest path length computed by Floyd-Warshall algorithm.
    """
    out = collections.defaultdict(dict)
    for u, v in itertools.product(valves, repeat=2):
        out[u.name][v.name] = 1 if u.name in v.connections else\
            0 if u.name == v.name else \
            math.inf

    for k, i, j in itertools.product(valves, repeat=3):
        out[i.name][j.name] = min(
            out[i.name][j.name],
            out[i.name][k.name] + out[k.name][j.name]
        )
    return out


def _get_costs_and_flows(valves: list[Valve]) -> tuple[Edges, Nodes]:
    """
    Organize the list of Valves and return the data as two dictionaries,
        - an edge dictionary that enumerates the distance between every pair of valves
        - and a node dictionary that enumerates node name and attributes.
    """
    valves_to_open: Nodes = {
        valve.name: (1 << i, int(valve.flow_rate))
        for i, valve in enumerate(
            filter(lambda valve: int(valve.flow_rate) > 0, valves)
        )
    }
    costs: Edges = _floyd_warshall(valves)
    return costs, valves_to_open


def _depth_first_search(costs: Edges, valves_to_open: Nodes, minutes: int = 30):
    """
    Implement depth-first search to open non-zero flow valves.
    Keep track of the maximum pressure released achieved by a set of valves opened.
    """
    State = collections.namedtuple(
        'State', ['current_valve', 'time_left', 'valves_opened', 'pressure']
    )

    initial: State = State('AA', minutes, 0, 0)
    frontier: list[State] = [initial]
    explored: dict[int, int] = {0: 0}   # {valves opened: pressure released by the valves}

    while frontier:
        v, time_left, opened, releasing = frontier.pop()
        if time_left <= 0:  # move on to the next item in frontier to backtrack
            continue
        for u in valves_to_open:
            (index, flow), cost = valves_to_open[u], costs[v][u]
            if not opened & index:
                newly_opened = opened | index
                new_time_left = time_left - cost - 1
                new_flow = releasing + (flow * new_time_left)
                frontier.append(
                    State(u, new_time_left, newly_opened, new_flow)
                )
                explored[newly_opened] = max(explored.get(newly_opened, 0), new_flow)
    return explored


def solve_part1(puzzle_input: list[Valve]) -> int:
    """
    Set up the arguments by passing the puzzle input to _get_costs_and_flows().
    Find the valves to open that would maximize the pressure released via _depth_first_search().
    Return the maximum pressure released by the possible states of visits.
    """
    args = _get_costs_and_flows(puzzle_input)
    visits = _depth_first_search(*args)
    return max(visits.values())


def solve_part2(puzzle_input: list[Valve]) -> int:
    """
    Like part 1, but explore the valves to open via _depth_first_search(minutes=26) because the first 4 minutes
    are consumed to teach the elephant and no valves can be opened during that time.
    Find the maximum
    """
    args = _get_costs_and_flows(puzzle_input)
    visits = _depth_first_search(*args, minutes=26)
    return max(
        elephant_work + my_work
        for elephant, elephant_work in visits.items()
        for me, my_work in visits.items()
        if not me & elephant
    )


if __name__ == '__main__':
    title = 'Day 16: Proboscidea Volcanium'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:

        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The most amount of pressure released in 30 minutes is {part1}.
        Part 2: The most amount of pressure released working with an elephant in 30 minutes is {part2}.
        """)
