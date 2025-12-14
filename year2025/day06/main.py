# year2025/day06/main.py
from pathlib import Path
from textwrap import dedent
from operator import add, mul
from functools import reduce
from collections import deque
from typing import Iterator, Iterable, Callable


def parse(txtfile: str) -> list[str]:
    return Path(txtfile).read_text().splitlines()


def organize_by_columns(
        lines: list[str],
        cephalopod_mode: bool = False) -> Iterator[Iterable[str]]:
    if not cephalopod_mode:
        rows = [line.strip().split() for line in lines]
        yield from zip(*rows)
    else:
        column = deque()
        for line in zip(*lines):
            *digits, symbol = line
            if not ''.join(line).strip():
                yield tuple(column)
                column.clear()
                continue
            if symbol.strip():
                column.append(symbol)
            column.appendleft(''.join(digits))
        yield tuple(column)


def get_operator(symbol: str) -> Callable:
    if symbol not in {'+', '*'}:
        raise ValueError(
            f'Cephalopod math does not use math operation {symbol}')
    return add if symbol == '+' else mul


def solve(*numbers, symbol: str = '+') -> int:
    return reduce(get_operator(symbol), map(int, numbers))


def solve_part1(data: list[str]) -> int:
    columns = list(organize_by_columns(data))
    return sum(
        solve(*numbers, symbol=symbol) 
        for *numbers, symbol in columns
    )


def solve_part2(data: list[str]) -> int:
    columns = list(
        organize_by_columns(data, cephalopod_mode=True))
    return sum(
        solve(*numbers, symbol=symbol) 
        for *numbers, symbol in columns
    )


if __name__ == '__main__':
    data = parse('input.txt')
    part1 = solve_part1(data)
    part2 = solve_part2(data)
    print(dedent(f"""\
        part1: the grand sum total is {part1}.
        part2: the correct grand sum total is {part2}.
    """))