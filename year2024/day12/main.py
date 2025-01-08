# year2024/day12/main.py
import sys
from pathlib import Path 
from typing import Collection, Iterator
from collections import UserDict

Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
NSWE = NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)
HEAD = '0'


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW], coord1[COLUMN] + coord2[COLUMN]
    )

def turn_clockwise(facing: Vector) -> Vector:
    clockwise = {
        NORTH: EAST,
        EAST: SOUTH,
        SOUTH: WEST,
        WEST: NORTH
    }
    return clockwise[facing]


class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to cell content.
    """

    def __init__(self, data: list[str]=(), directions: tuple[Vector, ...]=NSWE):
        grid = {
                (row, column): cell
                for row, line in enumerate(data)
                for column, cell in enumerate(line)
            }
        super().__init__(grid)
        self.directions = directions
    
    def __missing__(self, coordinate: Coordinate):
        return None
    
    def find_cells(self, targets: Collection) -> list[Coordinate]:
        return [
            coord
            for coord in self 
            if self[coord] in targets
        ]
    
    def get_neighbors(self, source: Coordinate) -> Iterator[Coordinate]:
        for direction in self.directions:
            if (destination := add_coordinates(source, direction)) in self:
                yield destination


def parse(txtfile) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def flood_fill(
        plot: Coordinate, 
        garden: Grid,
        current_region: set[Coordinate],
        explored: set[Coordinate]
    ) -> set[Coordinate]:
    """
    Flood fill from `plot` to neighboring plots in `garden`. 
    If the neighboring plot 
    When there are no more neighboring plots, return `current_region`.
    """
    if plot not in explored:
        current_region.add(plot)
        explored.add(plot)
        for neighbor in garden.get_neighbors(plot):
            if garden[plot] == garden[neighbor]:
                flood_fill(neighbor, garden, current_region, explored)
    return current_region


def measure_perimeter(region: set[Coordinate]) -> int:
    """
    Measure the perimter by counting how many of the four directions from each plot
    in the region are not in the region. 
    --------------------------------------------------
    e.g. Region "AAAA" has perimeter length 10 because 
        - the first "A" is missing neighbors in three directions (north, west, and south),
        - the second "A" two (north and south), 
        - the third "A" two (north and south), and 
        - the last "A" three (north, east, and south).
    The total number of non-neighbors is 3 + 2 + 2 + 3 = 10.
    ---------------------------------------------------
    Note that "neighbor" in this context can be a coordinate that is not in the grid. 
    This is why we can't use `Grid.get_neighbor()` method. 
    """
    return sum(
        add_coordinates(plot, direction) not in region
        for plot in region 
        for direction in NSWE
    )

def measure_area(region: set[Coordinate]) -> int:
    """Count the number of plots in each `region`."""
    return len(region)


def count_sides(region: set[Coordinate]) -> int:
    """
    Count the number of sides of `region` by first getting the 
    perimter length by `measure_perimter(region)`.
    Then for every plot's edge that is on the region's perimeter,
    if the edge extends to the right, subtract 1 from the perimeter.
    The number of sides is the number remaining after subtraction.
    ------------------
    e.g. Consider the region 'AAAA'. The perimter length is 10.
    The leftmost 'A' has 
        - a northern edge that extends right (east),
        - a southern edge that does not extend right (west),
        - a western edge that does not extend right (north).
    The first 'A' therefore contributes -1.
    The second 'A' plots has two edges that extend rightward
        and therefore contributes -2.
    By the same reason as above, the third 'A' plot also contributes -1.
    The last 'A' has 
        - a norther edge that does not extend right (east),
        - a southern edge that extends right (west),
        - an eastern edge that does not extned right (south).
    The last 'A' therefore contributes -2. 
    Therefore, the total number of sides is 10-1-2-2-1=10-6=4.
    """
    perimeter = measure_perimeter(region)

    def has_edge_extending_right(
            plot: Coordinate, 
            facing: Vector, 
            region: set[Coordinate]
        ) -> bool:
        edge = add_coordinates(plot, facing)
        right_neighbor = add_coordinates(plot, turn_clockwise(facing))
        right_neighbor_edge = add_coordinates(right_neighbor, facing)
        return (
            edge not in region and 
            right_neighbor in region and 
            right_neighbor_edge not in region
        )

    return perimeter - sum(
        has_edge_extending_right(plot, direction, region)
        for plot in region 
        for direction in NSWE
    )


def solve_part1(data) -> int:
    garden = Grid(data)
    explored = set()
    regions = [
        flood_fill(plot, garden, set(), explored)
        for plot in garden
        if plot not in explored
    ]
    return sum(
        measure_area(region) * measure_perimeter(region)
        for region in regions
    )


def solve_part2(data) -> int:
    garden = Grid(data)
    explored = set()
    regions = [
        flood_fill(plot, garden, set(), explored)
        for plot in garden
        if plot not in explored
    ]
    return sum(
        measure_area(region) * count_sides(region) 
        for region in regions
    )


if __name__ == '__main__':
    title = 'Day 12: Garden Groups'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The total price of fences is {part1}.
        Part 2: The discounted total price is {part2}.
        """)
