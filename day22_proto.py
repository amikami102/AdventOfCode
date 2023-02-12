"""
Day 22: Monkey Map
"""

import itertools
import math
import operator
import re

SAMPLE_INPUT = [
    "        ...#",
    "        .#..",
    "        #...",
    "        ....",
    "...#.......#",
    "........#...",
    "..#....#....",
    "..........#.",
    "        ...#....",
    "        .....#..",
    "        .#......",
    "        ......#.",
    "",
    "10R5L5R10L4R5L5",
]

PATTERN = re.compile(r"(\d+)|([LR])")


def _parse(lines):
    lines = iter(lines)
    board = [""]
    for line in lines:
        line = line.rstrip()
        if not line:
            break
        board.append(f" {line} ")
    board.append("")
    max_len = max(len(line) for line in board)
    for i, line in enumerate(board):
        board[i] = line.ljust(max_len, " ")
    moves = [
        int(match.group(1)) if match.group(1) else match.group(2)
        for match in re.finditer(PATTERN, next(lines))
    ]
    return board, moves


def _perimeter(board: list[str]):
    initial_x = board[1].index(".")
    x, y, direction = initial_x, 1, 0
    while True:
        yield x, y, direction
        forward_x = (x + 1, x, x - 1, x)[direction]
        forward_y = (y, y + 1, y, y - 1)[direction]
        if board[forward_y][forward_x] == " ":
            direction = (direction + 1) % 4
        else:
            left_x = (x + 1, x + 1, x - 1, x - 1)[direction]
            left_y = (y - 1, y + 1, y + 1, y - 1)[direction]
            if board[left_y][left_x] == " ":
                x, y = forward_x, forward_y
            else:
                x, y, direction = left_x, left_y, (direction - 1) % 4
        if x == initial_x and y == 1 and direction == 0:
            break


def _run(board, moves, warps):
    x, y, direction = board[1].index("."), 1, 0
    for move in moves:
        match move:
            case "L":
                direction = (direction - 1) % 4
            case "R":
                direction = (direction + 1) % 4
            case _:
                for _ in range(move):
                    next_x, next_y, next_direction = (
                        warps[x, y, direction]
                        if (x, y, direction) in warps
                        else (
                            (x + 1, x, x - 1, x)[direction],
                            (y, y + 1, y, y - 1)[direction],
                            direction,
                        )
                    )
                    if board[next_y][next_x] != ".":
                        break
                    x, y, direction = next_x, next_y, next_direction
    return 1000 * y + 4 * x + direction



def part2(lines):
    # pylint: disable=too-many-locals
    """
    >>> part2(SAMPLE_INPUT)
    5031
    """
    board, moves = _parse(lines)
    edges = [
        (key, list(edge))
        for key, edge in itertools.groupby(_perimeter(board), operator.itemgetter(2))
    ]
    #print(*edges, sep='\n')
    side_length = math.gcd(*(len(edge) for _, edge in edges))
    print(side_length)
    edges = [
        (direction, edge[i : i + side_length])
        for direction, edge in edges
        for i in range(0, len(edge), side_length)
    ]
    print(*edges, sep='\n')
    pairs = []
    while edges:
        i = 0
        while i < len(edges) - 1:
            direction1, edge1 = edges[i]
            direction2, edge2 = edges[i + 1]
            if (direction1 - direction2) % 4 == 1:
                pairs.append((edge1, edge2))
                edges[i : i + 2] = []
                edges[i:] = (
                    ((direction - 1) % 4, edge) for direction, edge in edges[i:]
                )
            else:
                i += 1
    print(*pairs, sep='\n')
    warps = {}
    for edge1, edge2 in pairs:
        for point1, point2 in zip(edge1, edge2[::-1]):
            x1, y1, direction1 = point1
            x2, y2, direction2 = point2
            warps[x1, y1, (direction1 - 1) % 4] = x2, y2, (direction2 + 1) % 4
            warps[x2, y2, (direction2 - 1) % 4] = x1, y1, (direction1 + 1) % 4
    print(*warps.items(), sep='\n')
    return _run(board, moves, warps)




if __name__ == "__main__":

    with open('day22_test.txt', 'r') as f:
        _lines = f.read().splitlines()
    print(part2(_lines))