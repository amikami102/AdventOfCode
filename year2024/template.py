# year2024/day##/main.py
import sys
from pathlib import Path 


def parse(txtfile):
    pass

def solve_part1(data):
    pass

def solve_part2(data):
    pass


if __name__ == '__main__':
    title = 'Day 5: Print Queue'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        print(data)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The number of XMASes is {part1}.
        Part 2: The number of X-MASes is {part2}.
        """)