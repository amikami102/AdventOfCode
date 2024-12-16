import sys
from pathlib import Path
from typing import Iterator
from collections import UserDict, namedtuple
from itertools import chain

Coordinate = tuple[int, int]
Vector = Coordinate
Beam = namedtuple('Beam', ['coordinate', 'direction'])


ROW, COLUMN = 0, 1
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
SPLITTERS: set[str] = {'|', '-'}
MIRRORS: set[str] = {'\\', '/'}


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    row1, col1 = coord1
    row2, col2 = coord2
    return row1 + row2, col1 + col2


class Grid(UserDict):
    """A 2D grid stored as {(row, column): cell}"""

    def __init__(self, grid: list[str]) -> None:
        self.size = len(grid), max(len(row) for row in grid)
        mapping = {
            (row, column): cell
            for row, line in enumerate(grid)
            for column, cell in enumerate(line)
        }
        super().__init__(mapping)
    
    def __missing__(self, nonexistent_coord: Coordinate) -> None:
        return


def split_beam(beam: Beam, splitter: str) -> Iterator[Beam]:
    """Split the `beam` according to the direction it hits the `splitter`."""
    if splitter == '|' and beam.direction in {RIGHT, LEFT}:
        directions = [UP, DOWN]
    elif splitter == '-' and beam.direction in {UP, DOWN}:
        directions = [LEFT, RIGHT]
    else:
        directions = [beam.direction]
    return (
            Beam(
                add_coordinates(beam.coordinate, direction), 
                direction
            )
            for direction in directions
        )


def reflect_beam(beam: Beam, mirror: str) -> Beam:
    """Change the direction of `beam` as it is reflected on `mirror`."""
    reflection = {
        '/':  {RIGHT: UP,   LEFT: DOWN, DOWN: LEFT,     UP: RIGHT},
        '\\': {RIGHT: DOWN, LEFT: UP,   DOWN: RIGHT,    UP: LEFT}
    }
    reflect_to = reflection[mirror][beam.direction]
    return Beam(add_coordinates(beam.coordinate, reflect_to), reflect_to)


def send_beam_through(
        contraption: Grid, start: Beam = Beam((0, 0), RIGHT)
    ) -> set[Coordinate]:
    """
    Send the `start` beam through throughout the `contraption` 
    and return which tiles are energized.
    """
    energized: set[Beam] = set()
    to_visit: list[Beam] = [start]

    while to_visit:
        beam = to_visit.pop()
        if beam.coordinate in contraption and beam not in energized:
            energized.add(beam)
            if (splitter := contraption[beam.coordinate]) in SPLITTERS:
                for candidate in split_beam(beam, splitter):
                    to_visit.append(candidate)
            elif (mirror := contraption[beam.coordinate]) in MIRRORS:
                to_visit.append(reflect_beam(beam, mirror))
            else:
                to_visit.append(
                    Beam(
                        add_coordinates(beam.direction, beam.coordinate),
                        beam.direction
                    )
                 )
    return {beam.coordinate for beam in energized}


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input) -> int:
    contraption = Grid(puzzle_input)
    return len(send_beam_through(contraption))


def solve_part2(puzzle_input) -> int:
    contraption = Grid(puzzle_input)
    nrows, ncols = contraption.size
    perimeter = \
        [Beam((i, 0), RIGHT) for i in range(nrows)] +\
        [Beam((0, j), DOWN) for j in range(ncols)] +\
        [Beam((nrows - 1, j), UP) for j in range(ncols)] +\
        [Beam((i, ncols - 1), LEFT) for i in range(nrows)]
    return max(
        len(send_beam_through(contraption, entry))
        for entry in perimeter
    )


if __name__ == '__main__':

    title = 'Day 16: The floor will be lava'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The number of energized tiles is {part1}.
        Part 2: The maximum number of energized tiles is {part2}.
        """)
