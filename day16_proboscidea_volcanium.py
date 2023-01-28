"""
Day 16: Proboscidea Volcanium
Solution borrowed liberally from
    - https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day16.py
    - https://github.com/mebeim/aoc/blob/8b5f3ef09cb6ddd98a99f8139dd3007ffa3e3d36/2022/solutions/day16.py
"""
import collections
import itertools
import re


Valve = collections.namedtuple('Valve', ['name', 'flow_rate', 'connected_to'])


def parse(line_to_parse: str) -> Valve:
    valve_pattern = re.compile(
        'Valve (?P<name>[A-Z]+) has flow rate=(?P<flow_rate>[0-9]+); tunnel[s]* lead[s]* to valve[s]* (?P<connected_to>.*)'
    )
    matched = re.match(valve_pattern, line_to_parse)
    return Valve(
        matched.group('name'),
        int(matched.group('flow_rate')),
        matched.group('connected_to').split(', ')
    )


def measure_distance(valve_list: list[Valve], do_iter: bool = False) -> dict :
    """
    Build a dictionary of pair of Valves and their distance.
    """
    edge_dict = collections.defaultdict(dict)
    for valve1, valve2 in itertools.product(valve_list, repeat=2):
        edge_dict[valve1.name][valve2.name] = 1 if valve2.name in valve1.connected_to else float('inf')

    # update distance by Floyd-Warshall algorithm
    if do_iter:
        for valve1, middle, valve2 in itertools.permutations(valve_list,3):
            edge_dict[valve1.name][valve2.name] = min(
                edge_dict[valve1.name][valve2.name],
                edge_dict[valve1.name][middle.name] + edge_dict[middle.name][valve2.name]
            )
    else:
        for valve1 in valve_list:
            for valve2 in valve_list:
                for middle in valve_list:
                    edge_dict[valve1.name][valve2.name] = min(
                        edge_dict[valve1.name][valve2.name],
                        edge_dict[valve1.name][middle.name] + edge_dict[middle.name][valve2.name]
                    )
    return edge_dict


with open('day16_input.txt', 'r') as f:
    valves = [
        parse(line.strip())
        for line in f
    ]

flows = {valve.name: valve.flow_rate for valve in valves if valve.flow_rate != 0}
I = {valve: 1<<i for i, valve in enumerate(flows)}
T = measure_distance(valves)
t1 = measure_distance(valves, True)
for key in T:
    for nested_key in T[key]:
        if t1[key][nested_key] != T[key][nested_key]:
            print(key, nested_key, t1[key][nested_key], T[key][nested_key])

def visit(v, budget, state, flow, answer):
    answer[state] = max(answer.get(state, 0), flow)
    for u in flows:
        newbudget = budget - T[v][u] - 1
        if newbudget <= 0:
            #print(I[u] & state, newbudget)
            continue
        if I[u] & state:
            continue
        visit(u, newbudget, state | I[u], flow + newbudget * flows[u], answer)
    return answer

# part 1
visit1 = visit('AA', 30, 0, 0, {})
print(f'The maximum amount of pressure released after 30 minutes in the tunnel is {max(visit1.values())}.')
# part 2
visit2 = visit('AA', 26, 0, 0, {})
combined_efforts = (
    elephant_pressure + my_pressure
    for elephant, elephant_pressure in visit2.items()
    for me, my_pressure in visit2.items()
    if not elephant & me
)
print(f'The maximum amount of pressure released from combined efforts with an elephant is {max(combined_efforts)}.')