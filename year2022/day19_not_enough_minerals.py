"""
-- Day 19: Not Enough Minerals --

Usage example:
    Advent_Of_Code/year2022 $ python day19_not_enough_minerals.py day19_test.txt day19_input.txt

Inspired by Peter Norvig's solution although there are faster solutions.
    - (u/4HbQ although this fundamentally relies on tuning the sorting key function and the threshold count) https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
    - (u/debnet based on above, but more readable and faster due to functools.cache)
    https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0vq06m/?utm_source=share&utm_medium=web2x&context=3

The three key ideas to solving the search problem are:
    - to prioritize building a geo robot over other actions (*);
    - except for geode crackers, to not built more robots than maximum necessary, which
        - for obsidian robot is the number of obsidians needed to build 1 geode cracker,
        - for clay robot is the number of clays needed to build 1 obsidian collector,
        - for ore robot is the number of ores needed by the robot that needs the most ores;
    - to prune search states that do not lead to the best known result.

*: Though the solution uses depth-first search, there is some prioritization done by popping out the action that builds a geo robot.
"""
import sys
import re
import pathlib
import functools
import collections
import math
from typing import *

Blueprint = collections.namedtuple(
    'Blueprint',
    ['id', 'ore_rbt_ORE', 'clay_rbt_ORE', 'obs_rbt_ORE', 'obs_rbt_CLAY', 'geo_rbt_ORE', 'geo_rbt_OBS']
)
Inventory = collections.namedtuple(
    'Inventory',
    ['time_left', 'ore', 'clay', 'obs', 'geo', 'ore_rbt', 'clay_rbt', 'obs_rbt', 'geo_rbt'],
    defaults=(0,)*9
)


def _update_inventory(state: Inventory, **kwargs) -> Inventory:
    """
    Return a new Inventory instance with the inventory values of `state`
    increased/decreased by **kwargs.
    """
    return Inventory(
        *tuple(p + q for p, q in zip(state, Inventory(**kwargs)))
    )


def parse(txt_filename: str):
    """Return the file content as list of Blueprints."""
    return [
        Blueprint(*tuple(map(int, re.findall(r'\d+', line))))
        for line in pathlib.Path(txt_filename).read_text().splitlines()
    ]


def depth_first_search(blueprint: Blueprint, total_minutes: int = 24):
    """
    Implement depth-first search to find how long it takes to create the most amount of geodes.
    """
    initial: Inventory = Inventory()._replace(time_left=total_minutes, ore_rbt=1)
    best: Inventory = initial
    upper_limit: Inventory = _set_limit(blueprint)
    frontier: list[Inventory] = [initial]
    explored: dict[tuple[int, ...], tuple[int, ...]] = {}

    while frontier:
        state = frontier.pop()  # the action that builds geo bot is popped first
        if state.geo > best.geo:
            best = state
        if state.time_left > 0 and not _is_pruned(state, explored, upper_limit, best):
            children = _down_the_branch(state, upper_limit, blueprint)
            frontier.extend(children)
    return best


def _set_limit(blueprint: Blueprint) -> Inventory:
    """
    Set limit for the maximum number of each type of robots to build
    according to this blueprint.
    """
    _, ore_rbt_ore, clay_rbt_ore, obs_rbt_ore, obs_rbt_clay, geo_rbt_ore, geo_rbt_obs = blueprint
    return Inventory(*(math.inf,) * 9)._replace(
        ore_rbt=max(ore_rbt_ore, clay_rbt_ore, obs_rbt_ore, geo_rbt_ore),
        clay_rbt=obs_rbt_clay,
        obs_rbt=geo_rbt_obs
    )


def _is_pruned(state: Inventory, explored: dict, upper_limit: Inventory, best: Inventory) -> bool:
    """
    Returns True if `state` is pruned so that we no longer deep-search further down this branch.
    A state is pruned if it is
        a) dominated by another branch that reached that state earlier
        b) the state will not make more geodes than another branch even if it makes a geode robot every minute it can.
    """
    branch_key: tuple[int, ...] = tuple(min(state, upper_limit))[:5]
    branch_value: tuple[int, ...] = state[5:]

    # check condition a)
    if branch_key in explored and \
            all(v <= v_alt for v, v_alt in zip(branch_value, explored[branch_key])):
        return True
    explored[branch_key] = branch_value
    max_geodes_down_this_branch: int = state.geo + \
        sum(range(state.geo_rbt, state.geo_rbt + state.time_left))  # sum(state.geo_rbt + i for i in range(state.time_left))
    return max_geodes_down_this_branch <= best.geo


def _down_the_branch(state: Inventory, upper_limit: Inventory, blueprint: Blueprint) -> list[Inventory]:
    """
    Return a list of eligible actions succeeding `state`.
    Actions considered are
        - collect resources and do nothing;
        - collect resources and build ore bot;
        - collect resources and build clay bot;
        - collect resources and build obsidian bot;
        - collect resources and built geode bot.
    All actions cost one minute. Other cost details are in `blueprint`.
    An action is eligible if
        a) there are enough resources AND
        b) the next bot created of type `bot` is less than or equal to `upper_limits[bot]`.
    """
    _, ore, clay, obs, geo, ore_rbt, clay_rbt, obs_rbt, geo_rbt = state
    *_, max_ore_rbt, max_clay_rbt, max_obs_rbt, max_geo_rbt = upper_limit
    _, ore_rbt_ore, clay_rbt_ore, obs_rbt_ore, obs_rbt_clay, geo_rbt_ore, geo_rbt_obs = blueprint

    successors: list[Inventory] = []
    collect_resources = _update_inventory(
        state,
        time_left=-1, ore=ore_rbt, clay=clay_rbt, obs=obs_rbt, geo=geo_rbt
    )
    successors.append(collect_resources)

    if ore_rbt < max_ore_rbt and ore >= ore_rbt_ore:
        successors.append(
            _update_inventory(collect_resources, ore_rbt=+1, ore=-ore_rbt_ore)
        )
    if clay_rbt < max_clay_rbt and ore >= clay_rbt_ore:
        successors.append(
            _update_inventory(collect_resources, clay_rbt=+1, ore=-clay_rbt_ore)
        )
    if obs_rbt < max_obs_rbt and ore >= obs_rbt_ore and clay >= obs_rbt_clay:
        successors.append(
            _update_inventory(collect_resources, obs_rbt=+1, ore=-obs_rbt_ore, clay=-obs_rbt_clay)
        )
    if geo_rbt < max_geo_rbt and ore >= geo_rbt_ore and obs >= geo_rbt_obs:
        successors.append(
            _update_inventory(collect_resources, geo_rbt=+1, ore=-geo_rbt_ore, obs=-geo_rbt_obs)
        )
    return successors


def solve_part1(puzzle_input: list[Blueprint]) -> int:
    """
    Return the sum of the blueprint id multiplied by the maximum number of geodes collected by the blueprints listed in `puzzle_input`.
    """
    return sum(blueprint.id * depth_first_search(blueprint, 24).geo for blueprint in puzzle_input)


def solve_part2(puzzle_input: list[Blueprint]) -> int:
    """
    Return the product of the maximum  number of geodes collected by the blueprints listed in `puzzle_input`.
    """
    return math.prod(
        depth_first_search(blueprint, 32).geo
        for blueprint in puzzle_input
    )

if __name__ == '__main__':
    title = 'Day 19: Not Enough Minerals'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data[:3])
        print(f"""{path}:
        Part 1: The total quality level of all blueprints is {part1}.
        Part 2: The product of max geodes produced by the first three blueprints is {part2}.
        """)
