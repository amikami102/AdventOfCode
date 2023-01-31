"""
Day 17: Pyroclastic Flow

Inspired by
    (very short code) https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day17.py

    (for a state hashing that's more elegant thant u/juanplopes's) https://www.reddit.com/r/adventofcode/comments/znykq2/comment/j0oa5tu/?utm_source=share&utm_medium=web2x&context=3
"""
import collections
from typing import Iterable, Iterator
import itertools
import functools

INITIAL_OFFSET_RIGHT: int = 2 + 1
INITIAL_OFFSET_TOP: int = 3 + 1

Point = collections.namedtuple('Point', ['x', 'y'])


def consume(iterator: Iterator, n: int) -> None:
    """
    Advance the iterator n-steps ahead. If n is None, consume entirely.
    """
    next(itertools.islice(iterator, n, n), None)


class Rock:
    """
    A class object representing a rock.

    Attributes
    ---
        shape : str
            description of the shape of the rock
        points: frozenset[Point]
            a set of coordinates representing the rock
        current_loc: Iterable[Point]
            the coordinates within the chamber that the rock currently takes up

    Methods
    ---
        update_loc(dx: int, dy: int) -> None
            update current_loc attribute by shifting the x coordinate of points by dx and y coordinate by dy
    """

    def __init__(self, shape: str, points: Iterable[Point]):
        self.shape = shape
        self.points: frozenset[Point] = frozenset(Point(*p) for p in points)
        self.current_loc = []

    def __repr__(self) -> str:
        return f'Rock shaped like {self.shape} at {self.current_loc}'

    def update_loc(self, dx: int, dy: int) -> None:
        old_loc = list(self.points) if not self.current_loc else self.current_loc.copy()
        self.current_loc = [Point(point.x + dx, point.y + dy) for point in old_loc]


class Chamber:
    """
    A class object representing the chamber through which rocks are falling through.

    Attributes
    ---
        WIDTH : int, fixed to 7
        INITIAL_HEIGHT : int, fixed to 3
        FLOOR: int, fixed to 0
        JETS : Iterator[str]
            an iterator that cycles through the jet pattern read from the input fi.

        height : int
            the height of the chamber, which will increase as more rocks pile on
        occupied: set[Point]
            a collection of points within the walls of the chamber that are occupied by rocks

    Methods
    ---
        free(point: Point) -> bool
            Return True if the point is not occupied by a rock, otherwise False.

        move(rock: Rock, dx: int, dy: int) -> bool
            Return True if the rock can move so that its current_loc coordinates are transposed by (dx, dy).

        place(rock: Rock) -> None
            Let the rock fall through the chamber until it can no longer move, and
            update the rock's current loc and add them to Chamber's set of occupied points.


    """

    def __init__(self, jet_pattern: str):
        self.WIDTH: int = 7
        self.INITIAL_HEIGHT: int = 3
        self.FLOOR: int = 0
        self.JETS: Iterator[str] = itertools.cycle(jet_pattern)
        self.current_jet: str = None
        self.height: int = 0
        self.occupied: set[Point] = set()

    def free(self, point: Point) -> bool:
        return (point not in self.occupied) and (point.y > self.FLOOR) and (0 < point.x < self.WIDTH + 1)

    def move(self, rock: Rock, dx: int, dy: int) -> bool:
        return all(
            self.free(Point(coord.x + dx, coord.y + dy)) for coord in rock.current_loc.copy()
        )

    def place(self, rock: Rock) -> None:
        dx, dy = 0, 0
        while True:
            self.current_jet = next(self.JETS)
            optional_shift = dx + (1 if self.current_jet == '>' else - 1)
            if self.move(rock, optional_shift, dy):
                dx = optional_shift
                # otherwise, do not change dx and do not exit the while-loop yet
            optional_fall = dy - 1
            if not self.move(rock, dx, optional_fall):
                # exit the while-loop when you can't fall any further
                break
            else:
                dy = optional_fall
        rock.update_loc(dx, dy)
        self.occupied.update(rock.current_loc)
        self.height = max(self.height, max(point.y for point in self.occupied))

    def check_for_pockets(self) -> int:
        sealed: int = functools.reduce(lambda i, j: i | j, (1 << (i + 1) for i in range(self.WIDTH)))
        top2rows: Iterable[Point] = [
            Point(x + 1, y)
            for (x, y) in itertools.product(range(self.WIDTH), (self.height, self.height - 1))
        ]
        occupied_x: int = functools.reduce(
            lambda i, j: i | j,
            (point.x for point in top2rows if self.free(point))
        )
        return occupied_x if occupied_x == sealed else 0


def solve(n_rocks: int, use_state_hash: bool = False) -> int:
    """
    Solve the problem by simulating n_rocks falling down the chamber.
    Optionally use state hashing by setting use_state_hash argument as True.
    Return the height of the chamber after n_rocks have fallen down.
    """
    cycles: dict[str, tuple[int, int]] = {}

    chamber: Chamber = Chamber(jets)
    chamber.occupied.clear()
    rocks: Iterator[dict] = itertools.cycle(rock_specs)
    counter: Iterator[int] = itertools.count()
    delta_heights = 0

    while next(counter) < n_rocks:
        current_rock = Rock(**next(rocks))
        current_rock.update_loc(INITIAL_OFFSET_RIGHT, INITIAL_OFFSET_TOP + chamber.height)
        chamber.place(current_rock)

        if use_state_hash:
            state = chamber.check_for_pockets()
            if not state:
                continue
            else:
                print(state)
                hash_key: str = f'{current_rock}|{chamber.current_jet}| {state}'
                if hash_key in cycles.keys():
                    old_height, prev_count = cycles[hash_key]

                    delta_steps = abs(n_rocks - prev_count)
                    delta_heights += (chamber.height - old_height) * delta_steps

                    consume(rocks, n=delta_steps)
                    consume(chamber.JETS, n=delta_steps)
                    consume(counter, n=delta_steps)

                cycles[hash_key] = (chamber.height, n_rocks)

    chamber.height += delta_heights
    return chamber.height


rock_specs: Iterable[dict] = [
    {
        'shape': '-',
        'points': [Point(*p) for p in ((0, 0), (1, 0), (2, 0), (3, 0))]
    },
    {
        'shape': '+',
        'points': [Point(*p) for p in ((0, 1), (1, 2), (1, 1), (2, 1), (1, 0))]
    },
    {
        'shape': '」',
        'points': [Point(*p) for p in ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))]
    },
    {
        'shape': 'l',
        'points': [Point(*p) for p in ((0, 0), (0, 1), (0, 2), (0, 3))]
    },
    {
        'shape': 'square',
        'points': [Point(*p) for p in ((0, 0), (1, 0), (0, 1), (1, 1))]
    }
]


with open('day17_input.txt', 'r') as f:
    jets = f.read().strip()



# part 1
N = 2022
print(solve(N), 'without state-hashing')
# part 2
N = 6000
print(solve(N, True), 'with state-hashing')





















