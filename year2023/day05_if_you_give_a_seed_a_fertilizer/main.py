from typing import *
import sys
from pathlib import Path
from collections import namedtuple
from itertools import batched
import re

MappingRange = namedtuple('MappingRange', ['range', 'offset'])


def extract_integers(string: str) -> tuple[int, ...]:
    return tuple(
        (int(num) for num in re.findall(r'\d+', string))
    )


def parse(filename: str) -> tuple:
    paragraphs = Path(filename).read_text().split('\n\n')
    return tuple(
        parse_paragraph(paragraph) 
        for paragraph in paragraphs
    )


def parse_paragraph(paragraph: str) -> Iterable:
    if paragraph.startswith('seeds:'):
        return extract_integers(paragraph)
    else:
        [_, *lines] = paragraph.splitlines()
        return [
            MappingRange(range(src, src + length), dest - src)
            for dest, src, length in map(extract_integers, lines)
        ]


def parse_seed_ranges(seeds: list[int]) -> list[range]:
    """(Part 2) Convert `seeds` into a list of ranges."""
    return [
        range(start, start + length)
        for start, length in batched(seeds, 2)
    ]


def convert(seed: int, mapping_ranges: list[MappingRange]) -> list[int]:
    """(Part 1) 
    Convert `seed` according to whether it falls in one of the `mapping_ranges`.
    """
    for mrange, offset in mapping_ranges:
        if seed in mrange:
            return seed + offset
    return seed


def find_intersecting_range(
        seed: range, mapping_ranges: Iterable[MappingRange]
    ) -> Optional[MappingRange]:
    """(Part 1)
    Return the first MappingRange in `mapping_ranges` that intersect with `seed`.
    """
    for mrange in mapping_ranges:
        if (mrange.range.start in seed) or (seed.start in mrange.range):
            return mrange
    return None, None


def convert_seed_ranges(
        input_ranges: list[range], 
        mapping_ranges: Iterable[MappingRange]
    ) -> Iterable[range]:
    """(Part 2) Convert all `input_ranges` into new ranges."""
    input_ranges = set(input_ranges)
    result: set[range] = set()
    while input_ranges:
        input_range = input_ranges.pop()
        output_range, offset = find_intersecting_range(input_range, mapping_ranges)
        if not output_range:
            result.add(input_range)
        else:
            start, stop =\
                max(input_range.start, output_range.start),\
                min(input_range.stop, output_range.stop)
            result.add(range(start + offset, stop + offset))
            if input_range.start < start:
                input_ranges.add(range(input_range.start, start))
            if stop < input_range.stop:
                input_ranges.add(range(stop, input_range.stop))
    return result


def solve_part1(puzzle_input) -> int:
    seeds, *mapping_ranges  = puzzle_input
    for ranges in mapping_ranges:
        seeds = [convert(seed, ranges) for seed in seeds]
    return min(seeds)


def solve_part2(puzzle_input):
    seeds, *mapping_ranges = puzzle_input
    seed_ranges = parse_seed_ranges(seeds)
    for mranges in mapping_ranges:
        seed_ranges = convert_seed_ranges(seed_ranges, mranges)
    return min(seed.start for seed in seed_ranges)


if __name__ == '__main__':
    title = 'Day 05: If you give a seed a fertilizer'
    print(title.center(50, '-'))

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}
        Part 1: The lowest location number is {part1}.
        Part 2: The lowest location number is {part2}.
        """)
        