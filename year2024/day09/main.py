# year2024/day##/main.py
import sys
from itertools import takewhile
from pathlib import Path 

FREE = '.'

def first_true(iterable, default=False, predicate=None):
    return next(
        (item for item in iterable if predicate(item)),
        default
    )


def parse(txtfile) -> tuple[int]:
    return tuple(int(num) for num in Path(txtfile).read_text())


def convert_to_layout(diskmap: tuple[int, ...]) -> list[str]:
    disksize = len(diskmap)
    layout = ''
    for file_id, map_index in enumerate(range(0, disksize, 2)):
        layout += str(file_id) * diskmap[map_index]
        if map_index + 1 < disksize:
            layout += FREE * diskmap[map_index + 1]
    return list(layout) 


def compress_layout(layout: list[str]) -> list[str]:
    disksize = len(layout)
    free_location = -1 
    block_location = disksize
    while True:
        free_location = first_true(
            range(free_location + 1, disksize),
            None,
            lambda i: layout[i] == FREE
        )
        block_location = first_true(
            range(block_location - 1, 0, -1),
            None,
            lambda i: layout[i] != FREE
        )
        if not free_location or free_location >= block_location:
            return layout 
        else:
            layout[free_location], layout[block_location] =\
                layout[block_location], FREE


def compute_checksum(layout: list[str]) -> int:
    #nonempties = takewhile(lambda space: space != FREE, layout)
    return sum(
        position * int(file_id) if file_id != FREE else 0
        for position, file_id in enumerate(layout)
    )
    
        
def solve_part1(data) -> int:
    disk_layout = convert_to_layout(data)
    compressed = compress_layout(disk_layout)
    return compute_checksum(compressed)


def solve_part2(data):
    pass


if __name__ == '__main__':
    title = 'Day 9: Disk Fragmenter'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""[Data from {txtfile}]
        Part 1: The checksum result is {part1}.
        Part 2: The new checksum result is {part2}.
        """)