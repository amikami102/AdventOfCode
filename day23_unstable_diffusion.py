"""
-- Day 23: Unstable Diffusion --

Inspired by Peter Norvig's solution (https://colab.research.google.com/github/norvig/pytudes/blob/main/ipynb/Advent-2022.ipynb#scrollTo=X7XYM8aji_oO)

The main block includes unit tests on a smaller grid.
"""
import sys
import pathlib
import collections
import functools
import itertools
from typing import *

Coord = tuple[int, int]     # (row, column)
Vector = Coord
Proposals = dict[Coord, list[Coord]]

ROW, COLUMN = 0, 1
GROUND, ELF = '.', '#'
ORTHOGONALS = North, South, West, East = (-1, 0), (1, 0), (0, -1), (0, 1)
DIAGONALS = NW, NE, SW, SE = (-1, -1), (-1, 1), (1, -1), (1, 1)
ZERO = (0, 0)
DIRECTIONS = ORTHOGONALS + DIAGONALS
PROPOSAL_RULES = (
    (North, NE, NW),
    (South, SE, SW),
    (West, NW, SW),
    (East, NE, SE),
)


def _add_vectors(vector1: Vector, vector2: Vector) -> Vector:
    return vector1[ROW] + vector2[ROW], vector1[COLUMN] + vector2[COLUMN]


def minmax(iterator: Iterator[int]) -> tuple[int, int]:
    it = list(iterator)
    MinMax = collections.namedtuple('MinMax', ['min', 'max'])
    return MinMax(min(it), max(it))


class Grid(dict):
    """A grid representation as mapping of (row, column) coordinate to cell value"""

    def __init__(self, grid: list[str] | dict[Coord, str],
                 directions: Sequence[Vector] = DIRECTIONS,
                 skip: tuple[str] = (),
                 default: str = KeyError):
        super().__init__()
        self.default = default
        self.directions = directions
        if isinstance(grid, list):
            self.update(
                {
                    (row, column): value
                    for row, line in enumerate(grid)
                    for column, value in enumerate(line)
                    if value not in skip
                }
            )
        else:
            self.update(grid)

    def __missing__(self, key) -> str:
        if self.default is KeyError:
            raise KeyError(f'{key} is not in grid')
        else:
            return self.default

    def get_neighbors(self, coord: Coord, cell_value: bool) -> Iterator[Coord]:
        if cell_value:
            yield from (self[_add_vectors(coord, direction)] for direction in self.directions)
        else:
            yield from (_add_vectors(coord, direction) for direction in self.directions)

    def __repr__(self) -> str:
        r0, r1 = minmax(coord[ROW] for coord in self.keys())
        c0, c1 = minmax(coord[COLUMN] for coord in self.keys())
        default = '' if self.default is KeyError else self.default
        return '\n'.join(
            ''.join(self.get((row, col), default) for col in range(c0, c1 + 1))
            for row in range(r0, r1 + 1)
        )


def elves_make_proposals(grid: Grid, rules: Iterable[tuple[Vector, ...]]) -> Proposals:
    """
    Return a dictionary mapping a coordinate on `grid` to elves, represented by their coordinates, that want to move there.
    """
    proposals: Proposals = collections.defaultdict(list)

    elves = [coord for coord, value in grid.items() if value == ELF]
    for elf in elves:
        if ELF in grid.get_neighbors(elf, True):
            check_for_this_elf = functools.partial(check_open_spaces, elf, grid)
            valid_direction: tuple[Vector, ...] = next(filter(check_for_this_elf, rules), None)
            if valid_direction:     # if there is a direction the elf can move to, move
                proposals[_add_vectors(elf, valid_direction[0])].append(elf)
            else:
                continue
        else:   # don't move if there aren't any elf in neighboring coords
            continue
    return proposals


def check_open_spaces(elf: Coord, grid: Grid, directions3: tuple[Vector, ...]) -> bool:
    """Return True if `elf` can move in one of `directions3` on `grid`."""
    return not any(
        grid[_add_vectors(elf, direction)] == ELF
        for direction in directions3
    )


def diffuse(grid: Grid) -> Iterator[Grid]:
    """Diffuse elves across `grid` until no one can move anymore."""
    rules = collections.deque(PROPOSAL_RULES, maxlen=4)
    yield grid      # yield the initial state
    while True:
        proposals: Proposals = elves_make_proposals(grid, rules)
        moves: dict[Coord, Coord] = {loc: next(iter(elves)) for loc, elves in proposals.items() if len(elves) == 1}
        if not moves:   # there are no more elves to move
            return
        for loc, elf in moves.items():
            grid[loc], grid[elf] = ELF, GROUND
        rules.rotate(-1)
        yield grid


def diffuse_n_rounds(grid: Grid, n: int):
    """Return the state of the grid AFTER `n` rounds of diffusion or return None."""
    # diffuse(grid) yields element from [grid, grid after 1 diffusion round, grid after 2 rounds, ...]
    # itertools.islice(diffuse(grid), n=2) would return [grid after 2 diffusion rounds, after 3 rounds, ...]
    # next(...) would return grid after 2 diffusion rounds
    return next(itertools.islice(diffuse(grid), n, None), None)


def count_ground_cells(grid: Grid) -> int:
    """
    Count the number of GROUND cells within the smallest rectangles
    that encloses all the elves on `grid` by subtracting the number of
    elves from the area of the rectangle.
    """
    elves: set[Coord] = {coord for coord, value in grid.items() if value == ELF}
    r0, r1 = minmax(elf[ROW] for elf in elves)
    c0, c1 = minmax(elf[COLUMN] for elf in elves)
    return (r1 - r0 + 1) * (c1 - c0 + 1) - len(elves)


def parse(txt_filename: str) -> list[str]:
    """Return the file content as list of strings"""
    return pathlib.Path(txt_filename).read_text().splitlines()


def solve_part1(puzzle_input: list[str]) -> int:
    """Count the number of ground cells after 10 rounds."""
    n = 10
    return count_ground_cells(
        diffuse_n_rounds(
            Grid(puzzle_input, default=GROUND),
            n
        )
    )


def solve_part2(puzzle_input: list[str]) -> int:
    """Count the number of the first round where no elf moves."""
    rounds = diffuse(Grid(puzzle_input, default=GROUND)) # (grid, grid after 1 diffusion, grid after 2 rounds, ...)
    # if it takes 19 rounds of diffusion until no elf can move, `rounds` would include 20 elements
    return len(list(rounds))


if __name__ == '__main__':
    title = 'Day 23: Unstable Diffusion'
    print(title.center(50, '-'))

    # test with smaller grid
    small = ['.....', '..##.', '..#..', '.....', '..##.', '.....']
    smallGrid = Grid(small, default=GROUND)
    NorthElf1, NorthElf2, SouthElf1, SouthElf2,  MiddleElf =\
        (1, 2), (1, 3), (4, 2), (4, 3), (2, 2)
    move_north, move_south = PROPOSAL_RULES[:2]

    # test that check_open_spaces() works
    assert check_open_spaces(NorthElf1, smallGrid, move_north)
    assert check_open_spaces(NorthElf1, smallGrid, move_north)
    assert not check_open_spaces(MiddleElf, smallGrid, move_north)
    assert check_open_spaces(MiddleElf, smallGrid, move_south)
    assert check_open_spaces(SouthElf1, smallGrid, move_north)
    assert check_open_spaces(SouthElf2, smallGrid, move_north)

    # test that elves_make_proposals() works
    smallProposals1 = elves_make_proposals(
            smallGrid,
            PROPOSAL_RULES
        )
    assert NorthElf1 in smallProposals1[_add_vectors(NorthElf1, North)]
    assert NorthElf2 in smallProposals1[_add_vectors(NorthElf2, North)]
    assert MiddleElf in smallProposals1[_add_vectors(MiddleElf, South)]
    assert SouthElf1 in smallProposals1[_add_vectors(SouthElf1, North)]
    assert SouthElf2 in smallProposals1[_add_vectors(SouthElf2, North)]

    # test that diffuse() and diffuse_n_rounds() work
    smallDiffusion1 = diffuse_n_rounds(smallGrid, 1)
    assert smallDiffusion1 == Grid(
        [
            '..##.',
            '.....',
            '..#..',
            '...#.',
            '..#..',
            '.....'
        ], default=GROUND
    )
    smallDiffusion2 = diffuse_n_rounds(Grid(small, default=GROUND), 2)
    assert smallDiffusion2 == Grid(
        [
            '.....',
            '..##.',
            '.#...',
            '....#',
            '.....',
            '..#..'
        ]
    )
    smallDiffusion3 = diffuse_n_rounds(Grid(small, default=GROUND), 3)
    assert smallDiffusion3 == Grid(
        [
            '..#..',
            '....#',
            '#....',
            '....#',
            '.....',
            '..#..'
        ]
    )
    assert len(list(diffuse(Grid(small, default=GROUND)))) == 4

    # test with larger grid
    large = parse('day23_test.txt')
    largeDiffusion2 = diffuse_n_rounds(Grid(large, default=GROUND), 2)
    assert count_ground_cells(largeDiffusion2) == count_ground_cells(
        Grid(
            [
                '..............',
                '.......#......',
                '....#.....#...',
                '...#..#.#.....',
                '.......#...#..',
                '...#..#.#.....',
                '.#...#.#.#....',
                '..............',
                '..#.#.#.##....',
                '....#..#......',
                '..............',
                '..............',
            ], default=GROUND
        )
    )

    for file in sys.argv[1:]:
        data = parse(file)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{file}:
        Part 1: The number of ground cells is {part1}.
        Part 2: The first round where no elf moves is {part2}.
        """)
