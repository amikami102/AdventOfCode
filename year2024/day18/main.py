# year2024/day##/main.py
import sys
from pathlib import Path 


def parse(txtfile):
    pass

def solve_part1(data, **kwargs):
    pass

def solve_part2(data):
    pass


if __name__ == '__main__':
    title = 'Day '
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        if txtfile == 'test.txt':
            kwargs = {'width': 7, 'height': 7}
        data = parse(txtfile)
        part1 = solve_part1(data, **kwargs)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The  is {part1}.
        Part 2: The  is {part2}.
        """)