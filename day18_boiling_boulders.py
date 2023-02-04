"""
--- Day 18: Boiling Boulders ---

Inspired by
    - https://www.reddit.com/r/adventofcode/comments/zoqhvy/comment/j1ry942/?utm_source=share&utm_medium=web2x&context=3

Idea for part 1:
A cube, (x1, y1, z1), is adjacent to another cube, (x2, y2, z2), if
x1 = x2 + 1 or x2 - 1, y1 = y2, z1 = z2 (i.e. cube 1 is just cube 2 shifted to the right or left by 1),
x1 = x2, y1 = y2 + 1 or y2 - 1, z1 = z2 (i.e. cube 1 is just cube 2 shifted forward or backward by 1),
x1 = x2, y1 = y2, z1 = z2 + 1 or z2 - 1 (i.e. cube 1 is just cube 2 shifted above or below by 1).

Idea for part 2:
Suppose that the lava droplet is enveloped by water on all six sides, which are planes of
min({x}), max({x}), min({y}), max({y}), min({z}), and max(z).
We want to create two versions of a list of outside cubes:
    - OUTSIDE_from_outside,
    - INSIDE_from_inside.
To build OUTSIDE_from_outside:
    Initialize a CANDIDATE queue by adding a cube we know to be exterior to input.
    While CANDIDATE queue is nonempty, do the following:
        1. Pop out a "cube" (x*, y*, z*) from CANDIDATE queue.
        2. Add (x*, y*, z*) to OUTSIDE_from_outside list .
        2. For each "cube" adjacent to (x*, y*, z*), {(p, q, r)}, check that
            a) it's not completely far away by confirming
                min({x}) - 1 <= p <= max({x}) + 1 AND
                min({y}) - 1 <= q <= max({y}) + 1 AND
                min({z}) - 1 <= r <= max({z}) + 1
            AND b) it's an exterior by confirming it's not one of the input cubes.
        3. If step 2 conditions (a) and (b) are confirmed, push the adjacent cube (p, q, r) to CANDIDATE queue.
TO build OUTSIDE_from_inside:
    Do the following over each input cube (x, y, z).
        1. For each cube adjacent to (x, y, z), {(x', y', z')}, check that
            a) it's not one of the input cubes;
            b) it's in the OUTSIDE set.
        2. If conditions 1a) and 1b) are met, add +1 to surface area count.
It's the cubes in OUTSIDE_from_inside that we know are
definitely adjacent to the innerCubes and are not one of innerCubes that
could be air pockets like (2, 2, 5) from the example.
Every time the same cube in _from_inside is confirmed to be in _from_outside, we are counting a unique surface area.
Therefore, the true surface area count is found by counting the times a cube in OUTSIDE_from_inside
is found in OUTSIDE_from_outside.
"""
import itertools
import collections
from typing import Iterable, Iterator, TypeVar

Cube = tuple[int, int, int]

with open('day18_input.txt', 'r') as f:
    innerCubes: frozenset[Cube] = frozenset([tuple(int(c) for c in cube.strip().split(',')) for cube in f])

xyz_shifts = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (-1, 0, 0), (0, -1, 0), (0, 0, -1)
]


def get_adjacent_cubes(cube: Cube) -> Iterator[Cube]:
    """ Get all six adjacent cubes for an input cube."""
    for shift in xyz_shifts:
        yield tuple(sum(coord) for coord in zip(cube, shift))

# part 1 4314
surface_areas_part1 = sum(
    1
    for inner_cube in innerCubes
    for neighbor in get_adjacent_cubes(inner_cube)
    if neighbor not in innerCubes
)
print(surface_areas_part1)


# part 2
def minmax(iterable: Iterable[int], **kwargs) -> tuple[int, int]:
    """
    Return minimum and maximum of input iterable.
    """
    my_list = list(iterable)  # to iterate over iterators twice
    MinMax = collections.namedtuple('minmax', ['min', 'max'])
    if not my_list:
        if 'default' in kwargs:
            return kwargs['default'], kwargs['default']
        else:
            raise ValueError('minmax is an empty iterable')
    else:
        return MinMax(
            min=min(my_list, key=kwargs.get('key', None)),
            max=max(my_list, key=kwargs.get('key', None))
        )


min_x, max_x = minmax((cube[0] for cube in innerCubes))
min_y, max_y = minmax((cube[1] for cube in innerCubes))
min_z, max_z = minmax((cube[2] for cube in innerCubes))

candidateQueue = collections.deque()
outside_from_outside: set[Cube] = set()
initial: Cube = (min_x - 1, min_y - 1, min_z - 1)
candidateQueue.append(initial)

while candidateQueue:
    candidate = candidateQueue.pop()
    outside_from_outside.add(candidate)
    for neighbor in get_adjacent_cubes(candidate):
        if (
                min_x - 1 <= neighbor[0] <= max_x + 1 and
                min_y - 1 <= neighbor[1] <= max_y + 1 and
                min_z - 1 <= neighbor[2] <= max_z + 1
        ) and neighbor not in innerCubes and neighbor not in outside_from_outside:
            candidateQueue.append(neighbor)
outside_from_inside = [
    neighbor
    for cube in innerCubes
    for neighbor in get_adjacent_cubes(cube)
    if neighbor not in innerCubes
]
surface_areas_part2 = sum(
    cube in outside_from_outside
    for cube in outside_from_inside
)
#answer 2444
print(surface_areas_part2)