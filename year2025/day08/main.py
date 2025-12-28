# year2025/day08/main.py
"""
Solution liberally borrowed from reddit user mnvrth's solution.
https://github.com/mnvr/aoc-25/blob/4ffe4e056e728c16fd5c2aee6df274c7a2d1c52f/08.py
"""
from pathlib import Path
from typing import Iterable, Collection, Optional
from itertools import combinations
from math import dist, prod
from operator import itemgetter

Junction = tuple[int, ...]

get_xcoord = itemgetter(0)

def parse(txtfile: str) -> Collection[Junction]:
    return [
        tuple(map(int, line.split(','))) 
        for line in
        Path(txtfile).read_text().splitlines()
    ]


def pair_and_sort_junctions(
        junctions: Iterable[Junction]
    ) -> list[tuple[Junction, Junction]]:
    return sorted(
        combinations(junctions, 2),
        key=lambda pair: dist(*pair))
    

def combine_circuits(
        junctions: Collection[Junction], 
        limit: Optional[int] = None
    ) -> set[frozenset[Junction]]|Iterable[Junction]:
    """
    For part 1, set `limit` to 10 for the example and 1000 for the real input;
    the function returns a set of fronzen sets of Junctions.

    For part 2, set `limit` to 0 or None;
    the function returns a length-2 tuple of Junctions.
    """
    paired = pair_and_sort_junctions(junctions)
    circuits = {frozenset([j]) for j in junctions}

    for i, pair in enumerate(paired, start=1):
        c1, c2 = (
            next((circuit for circuit in circuits if j in circuit))
            for j in pair)
        circuits -= {c1, c2}
        circuits.add(c1|c2)
        if limit and (i == limit):
            return circuits
        if (not limit) and (len(circuits) == 1):
            return pair
    return circuits


def solve_part1(data: Collection[Junction], **kwargs) -> int:
    circuits = combine_circuits(data, **kwargs)
    return prod(
        sorted(map(len, circuits), reverse=True)[:3]
    )


def solve_part2(data: Collection[Junction], limit=None) -> int:
    last_pair = combine_circuits(data, limit=limit)
    return prod(
        map(get_xcoord, last_pair)
    )

if __name__ == '__main__':
    print('############# day 8: playground #############')
    data = parse('input.txt')
    part1 = solve_part1(data, limit=1000)
    part2 = solve_part2(data)
    print(f"""
    part1: the product of the lengths of the three largest circuits is\n {part1}.
    part2: the product of the x-coordinates of the last junction pair is\n{part2}.
    """)