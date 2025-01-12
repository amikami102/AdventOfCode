#Grid.py
from collections import UserDict
from typing import Collection, Optional, Iterator, Iterable, MutableMapping
from operator import itemgetter

Coordinate = tuple[int, int]
Vector = Coordinate
ROW, COLUMN = 0, 1
NSWE = NORTH, SOUTH, WEST, EAST = (-1, 0), (1, 0), (0, -1), (0, 1)


def add_coordinates(coord1: Coordinate, coord2: Coordinate) -> Coordinate:
    return (
        coord1[ROW] + coord2[ROW], coord1[COLUMN] + coord2[COLUMN]
    )

def get_range(coordinates: Iterable[Coordinate], axis: int = ROW) -> range:
    return range(
        min(map(itemgetter(axis), coordinates)), 
        max(map(itemgetter(axis), coordinates)) + 1
    )


class Grid(UserDict):
    """
    A 2D grid represented as a mapping of (row, column) coordinate
    to cell content.
    """

    def __init__(
            self,
            data: list[str]|MutableMapping[Coordinate, str]=(), 
            directions: tuple[Vector, ...] = NSWE,
            skip: Collection[str] = set(),
            default: Optional[str]|KeyError = None
        ):
        self.skip = skip
        if isinstance(data, list):
            grid = {
                    (row, column): cell
                    for row, line in enumerate(data)
                    for column, cell in enumerate(line)
                    if cell not in self.skip
                }
        if isinstance(data, MutableMapping):
            grid = data
        super().__init__(grid)
        self.directions = directions
        self.default = default
    
    def __missing__(self, coordinate: Coordinate):
        if self.default is KeyError:
            raise KeyError(f'{coordinate} is missing')
        else:
            return None
    
    def find_cells(self, targets: Collection) -> list[Coordinate]:
        return [
            coord
            for coord in self 
            if self[coord] in targets
        ]
    
    def down_the_line(
            self, 
            current: Coordinate, direction: Vector
        ) -> Iterator[Coordinate]:
        """
        Yield all the coordinates in the grid 
        down the line in `direction` starting at `current`.
        """
        while self.get(current):
            yield current 
            current = add_coordinates(current, direction)
    
    def convert_to_list_of_rows(self, fill: str = '') -> list[list[str]]:
        """
        Convert the mapping to a list of rows.
        Use `fill` to fill in any missing coordinate.
        """
        row_range = get_range(self, ROW)
        column_range = get_range(self, COLUMN)
        return [
            [self.get((row, column), fill) for column in column_range]
            for row in row_range
        ]
    
    def display_grid(self, separator: str = '', fill: str = '') -> None:
        """
        Print the rows from `convert_to_list_of_rows()` method.
        `fill` will be used as the cell content of a missing coordinate.
        """
        for row in self.convert_to_list_of_rows(fill):
            print(separator.join(row))