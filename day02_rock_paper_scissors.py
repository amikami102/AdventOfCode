"""
--- Day 2: rock, paper, scissors ---

Usage example
    Advent_of_Code/year2022 $ python day02_rock_paper_scissors.py day02_test.txt day02_input.txt
"""
import sys
import pathlib
from typing import *

ROCK, PAPER, SCISSORS = 1, 2, 3
win_rules = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}
lose_rules = {v: k for k,v in win_rules.items()}
DRAW, LOSE, WIN = 3, 0, 6


def parse(txt_filename: pathlib.Path | str) -> list[tuple[str, ...]]:
    with open(txt_filename, 'r') as f:
        return [
            tuple(line.strip().split(' ')) for line in f
        ]


def solve_part1(rounds: Iterable[tuple[str, str]]) -> int:
    """
    They play A, B, or C, which are respectively Rock, Paper, Scissors.
    I play X, Y, or Z, which are respectively Rock, Paper, Scissors.
    The regular rock-paper-scissors rule applies.
    I score 0 if I lose, 3 if we draw, and 6 if I win plus the integer representing my play.

    Each string entry of data describes a round of rock-paper-scissors in the form '{opponent} {me}' except that opponent's play are encoded by either A, B, C and my play are either X, Y, or Z.
    Return my total score.
    """
    score = 0
    for opponent, me in rounds:
        opponent_play, my_play = 'ABC'.index(opponent) + 1, 'XYZ'.index(me) + 1
        score += (
            DRAW if opponent_play == my_play
            else WIN if win_rules[my_play] == opponent_play
            else LOSE) + my_play
    return score


def solve_part2(rounds: Iterable[tuple[str, str]]) -> int:
    """
    'X' = I lose, 'Y' = 'I draw', 'Z' = 'I win'
    Everything else is the same as part 1.
    Return the score if I play according to the scripted rounds.
    """
    score = 0
    for opponent, result in rounds:
        opponent_play = 'ABC'.index(opponent) + 1
        match result:
            case 'X':
                score += LOSE + win_rules[opponent_play]
            case 'Y':
                score += DRAW + opponent_play
            case 'Z':
                score += WIN + lose_rules[opponent_play]
    return score



if __name__ == '__main__':
    title = 'Day 02: Rock, Paper, Scissors'
    print(title.center(50, '-'))
    for path in sys.argv[1:]:
        print(f'{path}:')
        data = parse(path)
        part1 = solve_part1(data)
        part2 = solve_part2(data)
        print(f'Part 1: The total score as played according to the strategy guide is {part1}.')
        print(f'Part 2: The total score as played according to the new interpretation of the strategy guide is {part2}.')
