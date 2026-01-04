# year2025/day09/main.py
"""
Many part 2 solutions assumed that the polygon defined by 
the input's red tiles did not hae a concave side, which 
made me nervous to try on my input.
This solution is virtually a copy-paste of reddit user 4HbQ. 
I'm not too happy with their code's readability, but 
I wanted to be done with part 2. 

https://www.reddit.com/r/adventofcode/comments/1phywvn/comment/nt64t2d/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
"""
from pathlib import Path
from itertools import combinations, pairwise
from operator import itemgetter

ROW, COLUMN = 0, 1
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

Coordinate = RedTile = tuple[int, ...]
Line = tuple[Coordinate, Coordinate]

def add_coordinates(
        c1: Coordinate, c2: Coordinate) -> Coordinate:
    return (c1[ROW] + c2[ROW], c1[COLUMN] + c2[COLUMN])


def parse(txtfile: str) -> list[RedTile]:
    return [
        tuple(map(int, line.split(',')))
        for line in Path(txtfile).read_text().splitlines()]


def calculate_area(corner1: RedTile, corner2: RedTile) -> int:
    return (abs(corner1[ROW] - corner2[ROW]) + 1) *\
        (abs(corner1[COLUMN] - corner2[COLUMN]) + 1)


def solve_part1(data: list[RedTile]) -> int:
    largest_area = 0
    for c1, c2 in combinations(data, 2):
        largest_area = max(
            (calculate_area(c1, c2), largest_area))
    return largest_area


def solve_part2(data: list[RedTile]) -> int:
    opposite_corners = sorted(
        combinations(data, 2), 
        key=lambda pair: calculate_area(*pair),
        reverse=True)
    greenlines = sorted(
        pairwise(data + [data[0]]),
        key=lambda pair: calculate_area(*pair),
        reverse=True)
    for (r1, c1), (r2, c2) in opposite_corners:
        r1, r2 = sorted((r1, r2))
        c1, c2 = sorted((c1, c2))
        for (gr1, gc1), (gr2, gc2) in greenlines:
            gr1, gr2 = sorted((gr1, gr2))
            gc1, gc2 = sorted((gc1, gc2))
            if (gr1 < r2) and (gc1 < c2) and (gr2 > r1) and (gc2 > c1):
                break
        else:
            size = calculate_area((r1, c1), (r2, c2))
            break
    return size



if __name__ == '__main__':
    print('*********** day 9: movie theater ***********')
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(f"""
    part 1: the largest area of red tiles is {part1}.
    part 2: the largest rectangle within the polygon is {part2}.
    """)