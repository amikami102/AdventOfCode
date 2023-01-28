"""
--- Day 16: Proboscidea Volcanium ---
"""
import collections
import itertools
import re
import math

import pandas as pd

Valve = collections.namedtuple('Valve', ['name', 'flow_rate', 'connected_to'])


def parse(line: str) -> Valve:
    valve_pattern = re.compile(
        "Valve (?P<name>\w+) has flow rate=(?P<flow_rate>\d+); tunnel[s]* lead[s]* to valve[s]* (?P<connected_to>.*)"
    )
    matched = re.match(valve_pattern, line.strip())
    return Valve(
        matched.group('name'),
        int(matched.group('flow_rate')),
        matched.group('connected_to').split(', ')
    )


def weigh_edges(valves: list[Valve]) -> dict:
    """
    Build a dictionary of pair of Valves and their distance.
    """
    edge_dict = {
        (valve1.name, valve2.name): 1 if valve2.name in valve1.connected_to else math.inf
        for valve1, valve2 in itertools.permutations(valves, 2)
    }

    def floyd_warshall_algorithm(pair: tuple[str, str]) -> int:
        """
        Find the distance between valves i and j via Floyd-Warshall algorithm.
        Distance(i, j) = min(Distance(i, j, k) for all k)
        where Distance(i, j, k) = distance(i, k) + distance(k, j).
        """
        i, j = pair
        return min(
            edge_dict[pair],
            min(
                edge_dict[(i, k.name)] + edge_dict[(k.name, j)]
                for k in valves
                if k.name != i and k.name != j
            )
        )

    for key in edge_dict.keys():
        edge_dict.update({key: floyd_warshall_algorithm(key)})

    return edge_dict


class Tunnel:
    """
    A class object holding tunnel and methods to traverse through this tunnel system.

    Attributes
    ---
        nodes: pd.DataFrame
            rows of nodes (which are Valves) and their attributes
        edges: pd.DataFrame
            rows of edges and their attributes
        start: str, default='AA'
            the name of the node to start from
        time_limit: int, default=30
            the total number of minutes allowed for traversing the tunnel system
        time_to_open: int, default=1
            the number of minutes consumed opening a Valve
        tree_of_paths: dict[str, int]
            dictionary whose keys are 15-bit representation of the set of valves that have been opened
            and values are the maximum total pressure released with that set of valves open
            e.g. '0b0' means 0 valves are opened,
                '0b1' means 1 valve in position 1 << 0 is open,
                '0b10' means 1 valve in position 1 << 1 is open.

    Methods
    ---
        visit(current_node: str, time_remaining: int, current_pressure: int, history: int) -> None
            build a tree of tunnel traversal where the root of the tree is the starting node, 'AA'
    """

    def __init__(self, node_list: list[Valve]):
        self.nodes: pd.DataFrame = pd.DataFrame(
            [node._asdict() for node in node_list],
        ).set_index('name')
        self.edges: pd.DataFrame = pd.DataFrame(
            [
                [*k, v] for k, v in weigh_edges(node_list).items()
            ],
            columns=['src', 'dst', 'distance']
        ).set_index(['src', 'dst'])
        self.start = 'AA'
        self.time_limit: int = 30
        self.time_to_open: int = 1
        self.tree_of_paths = {}
        self.opened = {
            node: 1 << i for i, node in enumerate(self.nodes.loc[lambda x: x['flow_rate'] > 0].index)
        }

    def visit(self, current_node: str = None, time_remaining: int = None, current_pressure: int = None, history: int = None) -> None:
        # Initialize the placeholders if current_node is the starting node
        if current_node is None:
            current_node = self.start
            time_remaining, current_pressure, history = 30, 0, 0
        # Record the current history to self.tree_of_paths
        self.tree_of_paths[bin(history)] = max(self.tree_of_paths.get(bin(history), 0), current_pressure)
        # Collect edges extending from current_node to nodes of valves with nonzero flow rate extending
        next_edges = self.edges.xs(current_node) \
            .merge(
            self.nodes,
            left_index=True,
            right_index=True,
            how='left'
        ).loc[lambda x: x['flow_rate'] > 0]
        for next_node in next_edges.index:
            dist, frate = next_edges.loc[next_node, ['distance', 'flow_rate']]
            # Note that time_remaining -= dist + self.time_to_open doesn't work for some reason.
            time_remaining_new = time_remaining - (dist + self.time_to_open)
            # taking the intersection between idx and history will check whether idx is open
            if (time_remaining_new <= 0) or (self.opened[next_node] & history):
                continue
            else:
                # Note that current_pressure += time_remaining * frate fails to record this amount in self.answers
                pressure_updated = current_pressure + time_remaining_new * frate
                # open the valve by taking the union between history and idx
                self.visit(
                    next_node,
                    time_remaining_new,
                    pressure_updated,
                    history | self.opened[next_node]
                )


with open('day16_input.txt', 'r') as f:
    valves = [
        parse(line.strip())
        for line in f
    ]
tunnel = Tunnel(valves)
tunnel.visit()
print(f'The maximum amount of pressure released after 30 minutes in the tunnel is {max(tunnel.tree_of_paths.values())}.')