"""
--- Day 19: Not Enough Minerals ---

Inspired by
    - (u/4HbQ although this fundamentally relies on tuning the sorting key function and the threshold count) https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tvzgz/?utm_source=share&utm_medium=web2x&context=3
    - (u/debnet based on above, but more readable and faster due to functools.cache)
    https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0vq06m/?utm_source=share&utm_medium=web2x&context=3

"""
import functools
import re
import enum
from typing import NamedTuple, Iterator


class Materials:
    __slots__ = ['ore', 'clay', 'obsidian', 'geode']

    def __init__(self, *materials):
        self.ore, self.clay, self.obsidian, self.geode = materials

    def __iter__(self) -> Iterator[int]:
        yield from (self.ore, self.clay, self.obsidian, self.geode)

    @functools.cache
    def __lt__(self, other: 'Materials') -> bool:
        return any(left < right for left, right in zip(self.__iter__(), other.__iter__()))

    @functools.cache
    def __gt__(self, other: 'Materials') -> bool:
        return all(left > right for left, right in zip(self.__iter__(), other.__iter__()))

    @functools.cache
    def __ge__(self, other: 'Materials') -> bool:
        return all(left >= right for left, right in zip(self.__iter__(), other.__iter__()))

    @functools.cache
    def __le__(self, other: 'Materials') -> bool:
        return any(left <= right for left, right in zip(self.__iter__(), other.__iter__()))

    @functools.cache
    def __add__(self, other: 'Materials') -> 'Materials':
        return Materials(*(left + right for left, right in zip(self.__iter__(), other.__iter__())))

    @functools.cache
    def __sub__(self, other: 'Materials') -> 'Materials':
        return Materials(*(left - right for left, right in zip(self.__iter__(), other.__iter__())))


class Blueprint(NamedTuple):
    """
    A namedtuple holding the blueprint recipe.
    Each production tuple contains
        - a 1x4 array of costs and
        - a 1x4 array of output where all the entries are zero except for 1 at the material's index position
        (e.g. ore production's second array is [1, 0, 0, 0], clay production's [0, 1, 0, 0]).
    no_production represents the costs and result of making nothing.
    """
    ore_production: tuple[Materials, Materials]
    clay_production: tuple[Materials, Materials]
    obsidian_production: tuple[Materials, Materials]
    geode_production: tuple[Materials, Materials]
    no_production: tuple[Materials, Materials] = \
        Materials(0, 0, 0, 0), Materials(0, 0, 0, 0)


def parse(line: str) -> tuple[int, Blueprint]:
    """Return a dictionary object representing a blueprint."""
    id, ore_rbt_ore, clay_rbt_ore, obsidian_rbt_ore, obsidian_rbt_clay, geode_rbt_ore, geode_rbt_obsidian = \
        map(int, re.findall(r'\d+', line))
    return id, Blueprint(
        (Materials(ore_rbt_ore, 0, 0, 0), Materials(1, 0, 0, 0)),
        (Materials(clay_rbt_ore, 0, 0, 0), Materials(0, 1, 0, 0)),
        (Materials(obsidian_rbt_ore, obsidian_rbt_clay, 0, 0), Materials(0, 0, 1, 0)),
        (Materials(geode_rbt_ore, 0, geode_rbt_obsidian, 0), Materials(0, 0, 0, 1))
    )


def run(blueprint: Blueprint, minutes: int, threshold: int) -> int:
    states = [
        (
            Materials(0, 0, 0, 0),  # the resources
            Materials(1, 0, 0, 0)  # the robots
        )
    ]
    for _ in range(minutes):
        next_to_do: list = []
        for resources, robots in states:
            for costs, new in blueprint:
                if all(c <= r for r, c in zip(resources, costs)):  # can we afford this production?
                    will_have = resources + robots - costs
                    will_make = robots + new
                    next_to_do.append((will_have, will_make))
        states = sorted(next_to_do, reverse=True, key=lambda sequences: tuple(zip(*sequences))[::-1])[:threshold]
    return max(resources.geode for resources, _ in states)


with open('day19_input.txt', 'r') as f:
    blueprints = list(map(parse, f))
part1: int = sum(run(blueprint, 24, 1000) * i for i, blueprint in blueprints)
print(part1)    # 1466
part2: int = functools.reduce(
    lambda x, y: x * y,
    (run(blueprint, 32, 9000) for i, blueprint in blueprints if i < 4)
)
print(part2)    # 8250