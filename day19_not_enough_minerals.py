"""
--- Day 19: Not Enough Minerals ---

Inspired by
    - (u/4HbQ although this fundamentally relies on tuning the sorting key function and the threshold count) https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
    - (u/debnet based on above)
    https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0vq06m/?utm_source=share&utm_medium=web2x&context=3

Incorporating functools.cache like u/debnet would make it much faster.

"""
import functools
import re
import enum
from typing import NamedTuple
from dataclasses import dataclass, field
from functools import cache
import numpy as np


class Material(enum.IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


class Blueprint(NamedTuple):
    """
    A namedtuple holding the blueprint recipe.
    Each production tuple contains
        - a 1x4 array of costs and
        - a 1x4 array of output where all the entries are zero except for 1 at the material's index position
        (e.g. ore production's second array is [1, 0, 0, 0], clay production's [0, 1, 0, 0]).
    no_production represents the costs and result of making nothing.
    """
    ore_production: tuple[np.array, np.array]
    clay_production: tuple[np.array, np.array]
    obsidian_production: tuple[np.array, np.array]
    geode_production: tuple[np.array, np.array]
    no_production: tuple[np.array, np.array] = np.array([0, 0, 0, 0]), np.array([0, 0, 0, 0])


def parse(line: str) -> tuple[int, Blueprint]:
    """Return a dictionary object representing a blueprint."""
    id, ore_rbt_ore, clay_rbt_ore, obsid_rbt_ore, obsid_rbt_clay, geode_rbt_ore, geode_rbt_obsid = map(int, re.findall(
        r'\d+', line))
    return id, Blueprint(
        (np.array([ore_rbt_ore, 0, 0, 0]), np.array([1, 0, 0, 0])),
        (np.array([clay_rbt_ore, 0, 0, 0]), np.array([0, 1, 0, 0])),
        (np.array([obsid_rbt_ore, obsid_rbt_clay, 0, 0]), np.array([0, 0, 1, 0])),
        (np.array([geode_rbt_ore, 0, geode_rbt_obsid, 0]), np.array([0, 0, 0, 1]))
    )


def run(blueprint: Blueprint, minutes: int) -> int:
    current = [
        (
            np.array([0, 0, 0, 0]),  # the resources
            np.array([1, 0, 0, 0])  # the robots
        )
    ]
    sortkey = lambda arrs: tuple(zip(*arrs))[::-1]
    for _ in range(minutes):
        next_to_do = []
        for resources, robots in current:
            for costs, new in blueprint:
                if all(c <= r for r, c in zip(resources, costs)):     # can we afford this production?
                    will_have = resources + robots - costs
                    will_make = robots + new
                    next_to_do.append((will_have, will_make))
        current = sorted(next_to_do, reverse=True, key=sortkey)[:10000]
    return max(resources[Material.GEODE] for resources, _ in current)


with open('day19_input.txt', 'r') as f:
    # part1 = sum(
    #     run(blueprint, 24) * i
    #     for i, blueprint in map(parse, f)
    # )
    part2 = functools.reduce(
        lambda x,y: x*y,
        (run(blueprint, 32)
        for i, blueprint in map(parse, f)
        if i < 4)
    )
print(part1)
print(part2)