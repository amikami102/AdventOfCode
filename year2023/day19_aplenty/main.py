"""
Consulted David Brownman's writeup for how to solve Part 2:
https://advent-of-code.xavd.id/writeups/2023/day/19/, accessed 2024-01-14.
Adapted code from Peter Norvig's notebook:
https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2023.ipynb, accesed 2024-01-14.
"""
import sys
from pathlib import Path
from collections import namedtuple
import re
from operator import lt as less_than, gt as greater_than


Part = namedtuple('Part', 'x,m,a,s')
Rule = namedtuple('Rule', ['category', 'operator', 'threshold', 'destination'])


ACCEPT, REJECT = 'A', 'R'
OPERATORS = {'>': greater_than, '<': less_than}
START, STOP = 1, 4001
RATING_RE = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')
WORKFLOW_RE = re.compile(r'([a-z]+){(.+)}')
RULE_RE = re.compile(r'([xmas])([\<\>])(\d+):(\w+)')


def intersect_ranges(range1: range, range2: range) -> range:
    return range(
        max(range1.start, range2.start),
        min(range1.stop, range2.stop)
    )


def parse(txtfile: str) -> tuple[dict[str, list[Rule]], list[Part]]:
    lines1, lines2 = (
        paragraph.splitlines()
        for paragraph in Path(txtfile).read_text().split('\n\n')
    )
    return dict([parse_workflow(line) for line in lines1]),\
        [parse_part(line) for line in lines2]


def parse_workflow(line: str) -> tuple[str, list[Rule]]:
    name, rules = WORKFLOW_RE.match(line).groups()
    return name, [parse_rule(rule) for rule in rules.split(',')]


def parse_rule(substring: str) -> Rule|str:
    if match := RULE_RE.match(substring):
        category, op, threshold, dest = match.groups()
        return Rule(category, OPERATORS[op], int(threshold), dest)
    else:
        return substring


def parse_part(line: str) -> Part:
    return Part(
        *(int(group) for group in RATING_RE.match(line).groups())
    )


def pass_through(part: Part, rules: list[Rule]) -> str:
    """(Part 1)
    Pass through `part` through `rules` and return the final destination.
    """
    *rules, final = iter(rules)
    for rule in rules:
        if rule.operator(getattr(part, rule.category), rule.threshold):
            return rule.destination
    return final


def is_accepted(
        part: Part, workflows: dict[str, list[Rule]], destination: str = 'in'
    ) -> bool:
    """(Part 1)
    Starting at the workflow named 'in', pass `part` through the workflows 
    recursively until it is accepted or rejected.
    Return True if `part` is accepted, False otherwise.
    """
    if destination in {ACCEPT, REJECT}:
        return destination == ACCEPT
    next_destination = pass_through(part, workflows[destination])
    return is_accepted(part, workflows, next_destination)


def split_rating(rating: Part, rule: Rule) -> tuple[str, Part, Part]:
    """(Part 2)
    Split `rating` into two ratings, one that passes the if-else rule and another
    that fails. Return the tuple of the destination for the passing rating, 
    the passing rating, and the failed rating.
    """
    current_range = getattr(rating, rule.category)
    if rule.operator == less_than:
        true_range = intersect_ranges(current_range, range(START, rule.threshold))
        false_range = intersect_ranges(current_range, range(rule.threshold, STOP))
    elif rule.operator == greater_than:
        true_range = intersect_ranges(current_range, range(rule.threshold + 1, STOP))
        false_range = intersect_ranges(current_range, range(START, rule.threshold + 1))
    return (
        rule.destination, 
        rating._replace(**{rule.category: true_range}),
        rating._replace(**{rule.category: false_range})
    )


def send_through_workflows(rating: Part, workflows, destination: str = 'in'):
    """(Part 2)
    Recurisvely yield `rating` that gets accepted.
    """
    if destination == ACCEPT:
        yield rating
    elif destination == REJECT:
        pass
    else:
        *rules, final = iter(workflows[destination])
        for rule in rules:
            next_destination, true_result, rating = split_rating(rating, rule)
            yield from send_through_workflows(true_result, workflows, next_destination)
        yield from send_through_workflows(rating, workflows, final)


def count_combination(rating: Part) -> int:
    """(Part 2) Count the rating combinations."""
    return len(rating.x) * len(rating.m) * len(rating.a) * len(rating.s)


def construct_rating() -> Part:
    """(Part 2)
    Construct `Part` whose ratings are all ranges between START and STOP.
    """
    ranges = [range(START, STOP)] * 4
    return Part(*ranges)


def solve_part1(puzzle_input) -> int:
    workflows, parts = puzzle_input
    return sum(
        part.x + part.m + part.a + part.s 
        for part in parts 
        if is_accepted(part, workflows)
    )


def solve_part2(puzzle_input) -> int:
    workflows, _ = puzzle_input
    rating = construct_rating()
    return sum(
        count_combination(accepted)
        for accepted in send_through_workflows(rating, workflows)
    )

if __name__ == '__main__':

    title = 'Day 19: Aplenty'
    print(title.center(50, '-'))

    part = parse_part('{x=787,m=2655,a=1222,s=2876}')
    assert part == Part(x=787, m=2655, a=1222, s=2876)
    name, rules = parse_workflow('hdj{m>838:A,pv}')
    assert name == 'hdj'
    assert rules[0] == Rule(category='m', operator=greater_than, threshold=838, destination='A')
    assert pass_through(part, rules) == 'A'
    
    rating = construct_rating()
    _, true_result, false_result = split_rating(rating, rules[0])
    assert true_result.m == range(839, 4001)
    assert true_result.a == range(1, 4001)
    assert false_result.m == range(1, 839)
    assert false_result.a == range(1, 4001)

    for txtfile in sys.argv[1:]:
        data = parse(txtfile)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f"""{txtfile}:
        Part 1: The sum of the ratings of accepted parts is {part1}.
        Part 2: The number fo rating combinations that will be accepted is {part2}.
        """)
