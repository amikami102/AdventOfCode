import sys
from pathlib import Path
import re
from typing import Iterator
from dataclasses import dataclass, field
from collections import defaultdict

X, Y, Z = 0, 1, 2


Coordinate = tuple[int, int, int]


@dataclass
class Brick:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int
    ground: bool = field(init=False)

    def __post_init__(self):
        self.x0, self.x1 = sorted((self.x0, self.x1))
        self.y0, self.y1 = sorted((self.y0, self.y1))
        self.z0, self.z1 = sorted((self.z0, self.z1))
        self.ground = self.z0 == 1
    

    def bottom_surface(self) -> Iterator[Coordinate]:
        return (
            (x, y, None) 
            for x in range(self.x0, self.x1 + 1)
            for y in range(self.y0, self.y1 + 1)
        )


@dataclass
class Stack:


    





def read_snapshot(lines: list[str]) -> list[Brick]:
    return [
        Brick(*extract_integers(line))
        for line in lines
    ]


def extract_integers(text: str) -> tuple[int, ...]:
    return tuple(
        (int(num) for num in re.findall(r'\d+', text))
    )


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def solve_part1(puzzle_input) -> int:
    pass


def solve_part2(puzzle_input) -> int:
    pass


if __name__ == '__main__':
    title = 'Day 06: Wait for it'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The product is {part1}.
        Part 2: The number of ways to win this long race is {part2}.
        """)
