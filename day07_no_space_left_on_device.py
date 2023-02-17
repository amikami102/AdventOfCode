"""
-- Day 07: No Space Left on Device

Usage example:
    Advent_of_Code/year2022 $ python day07_no_space_left_on_device.py day07_test.txt day07_input.txt
"""
import sys
import collections
import itertools
import re

CD_PATTERN = re.compile(r'^\$ cd (?P<dir>\S+)$')
LS_PATTERN = re.compile(r'^\$ ls$')
FILE_PATTERN = re.compile(r'^(?P<filesize>\d+) (?P<filename>\S+)$')
DIR_PATTERN = re.compile(r'^dir (?P<dir>\w+)$')


def parse(txt_filename: str) -> list[str]:
    """
    Return a list of strings.
    """
    with open(txt_filename, 'r') as f:
        return f.read().splitlines()


def _walk(commands: list[str]) -> dict[str, int]:
    """
    Return a mapping of directory to the total of their content file sizes.
    The commands walk down a tree until it reaches an end of a branch before it backtracks to the last fork
    that leads to another unopened branch.
    * Assume that the same directory is never opened twice.
    * Assume that there can be the same directory name can be used in different parent folders.
    """
    directory_sizes: dict[str, int] = collections.defaultdict(int)
    branch_path = collections.deque(['/'])
    for command in commands:
        if command.startswith('$ cd'):
            dirname = re.match(CD_PATTERN, command).group('dir')
            match dirname:
                case '/':
                    branch_path = collections.deque(['/'])
                case '..':
                    branch_path.pop()
                case _:
                    branch_key = '/'.join((branch_path[-1], dirname))
                    branch_path.append(branch_key)
                    directory_sizes[branch_key] += 0
        elif command.startswith('$ ls') or command.startswith('dir'):
            # don't do anything
            continue
        else:
            for key in branch_path:
                directory_sizes[key] += int(re.match(FILE_PATTERN, command).group('filesize'))
    return directory_sizes


def solve_part1(puzzle_input: list[str]) -> int:
    """
    The puzzle input is the terminal commands, which will be passed into _walk() to
    get a mapping of directories and their content file sizes.
    Return the sum of sizes of directories whose total size is at most MAX_SIZE.
    """
    directory_sizes = _walk(puzzle_input)
    MAX_SIZE: int = 100000
    return sum(size for size in directory_sizes.values() if size <= MAX_SIZE)


def solve_part2(puzzle_input: list[str]) -> int:
    """
    Like solve_part1(), get a mapping of directory paths and their content file sizes
    by passing the puzzle input into _walk().
    Return the size of the smallest directory that would free up enough space so that
    the disk can meet the required unused space out of the total disk space.
    """
    directory_sizes = _walk(puzzle_input)
    TOTAL, REQUIRED_UNUSED = 70000000, 30000000
    min_dir_to_delete = REQUIRED_UNUSED - (TOTAL - directory_sizes['/'])
    return min(
        itertools.filterfalse(
            lambda v: v < min_dir_to_delete,
            directory_sizes.values()
        )
    )


if __name__ == '__main__':
    title = 'Day 07: No Space Left on Device'
    print(title.center(50, '-'))

    for path in sys.argv[1:]:
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{path}:
        Part 1: The size of the largest directory that is at most 100000 is {part1}.
        Part 2: The size of the smallest directory that would free up enough space to meet the required unused disk space is {part2}.
        """)