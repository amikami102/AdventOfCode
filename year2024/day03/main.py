# year2024/day03/main.py
import sys
import re
from pathlib import Path
from itertools import takewhile

MEMORY_PATTERN = re.compile(r"""
    mul
    \(
    (\d{1,3})   # first number
    ,
    (\d{1,3})  # second number
    \)
    """, re.X
)
INSTRUCTION_PATTERN = re.compile(r"""
    (don't\(\))
    |
    (do\(\))
    """, re.X)


def parse(txtfile: str) -> str:
    return Path(txtfile).read_text().strip()


def solve_part1(data) -> int:
    return sum(
        int(match.group(1)) * int(match.group(2))
        for match in MEMORY_PATTERN.finditer(data)
    )


def solve_part2(data) -> int:
    enabled = True 
    running_total = 0
    data = data + 'do()'
    while match := INSTRUCTION_PATTERN.search(data):
        start, end = match.span()
        if enabled:
            clause = data[:start]
            running_total += solve_part1(clause)
        enabled = match.group() == "do()"
        data = data[end:]
    return running_total
    

if __name__ == '__main__':
    title = 'Day 3: Mull It Over'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The sum of the multiplications is {part1}.
        Part 2: The sum of the results of enabled multiplications is {part2}.
        """)