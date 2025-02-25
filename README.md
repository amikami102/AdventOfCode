## Description 🎄

This is my repository for [Advent of Code](https://adventofcode.com/) solutions year by year. I write my solutions in Python and try to only use built-in modules and methods. I borrowed the Python script template from [a *Real Python* article](https://realpython.com/python-advent-of-code/#the-structure-of-a-solution) where each day's script will have three main functions `parse()`, `solve_part1()`, and `solve_part2()` that are used in the `if __name__ == '__main__'` block. 

## Year 2024

I was late to the party and started from day 1 on December 21st, but this seems harder than the last two years. I completely skipped day 9, and something is wrong with my part 2 solutions for day 14, 16, and 16. 

## Year 2023 

2023 was not a good year for me. I had spent the whole year applying to jobs (north of 600 job applications, which is still less than the number of applications I submitted in 2020--it was a slow job market), so by the time December rolled around, I didn't even have the bandwidth to do anything for fun. I started the 2023 advent late in April because I was bored during the day when I was working remotely for a contract position. I got through until day 22, but I don't think I'll finish all of it.

## Year 2022

This was my first year doing AoC. I got through the first ten days without much sweat thanks to my familiarity with `itertools` and `collections` methods thanks to Python Morsels. 

Starting around day 16, to my frustration, I had to peek at other Python solutions posted on Reddit. By the time I got to day 20 I really wanted to be done (January was almost over), so I would go straight to Reddit and read as many solutions as I can first before solving. Rarely would a single solution strike me as ideal, so my solutions took bits and pieces from various sources with my annotations and tests. During this process, I came across [Peter Norvig] and [his elegant AoC solution](https://github.com/norvig/pytudes). 

My first year of Advent of Code was a dense learning experience. Since I didn't have a computer science background, this was my first time writing path-finding algorithms (days [12](https://github.com/amikami102/AdventOfCode/blob/1386eac2219ace58f82ba13bb7199d6a72ed0db9/year2022/day12_hill_climbing_algorithm.py), [13](https://github.com/amikami102/AdventOfCode/blob/bbe95de0983d5c93506494581cafc482190cf01d/year2022/day13_distress_signal.py), [16](https://github.com/amikami102/AdventOfCode/blob/54bdad0e0f1b672e53f3b69b3efd9ab8cf8fc041/year2022/day16_proboscidea_volcanium.py), [18](https://github.com/amikami102/AdventOfCode/blob/1710c6b423aab554e832e2c30b737a290420c58c/year2022/day18_boiling_boulders.py), and [24](https://github.com/amikami102/AdventOfCode/blob/54bdad0e0f1b672e53f3b69b3efd9ab8cf8fc041/year2022/day24_blizzard_basin.py)). I got to practice writing recursive functions (days [21](https://github.com/amikami102/AdventOfCode/blob/54bdad0e0f1b672e53f3b69b3efd9ab8cf8fc041/year2022/day21_moneky_math.py) and [25](https://github.com/amikami102/AdventOfCode/blob/54bdad0e0f1b672e53f3b69b3efd9ab8cf8fc041/year2022/day25_full_of_hot_air.py)). And though I didn't adopt them in my final scripts, I saw some creative solutions that navigated grids with [bitwise operators](https://github.com/juanplopes/advent-of-code-2022/blob/6794122df32a857827e0c49871e848afe62cff18/day16.py) and complex numbers to represent up-down-left-right directions. I'd love to keep doing Advent of Code as a holiday tradition. My thanks to [Eric Wastl](https://adventofcode.com/2022/about) for writing these whimsical puzzles, and a hat tip to [Mike Driscoll](https://twitter.com/driscollis?s=20) from whose tweet I learned the existence of Advent of Code.

Here is a table cataloging of methods, modules, and problem-solving frameworks I learned. 🎁

| day | tags |
|:--:| :---|
| 01 | `itertools.groupby` | 
| 03 | `grouper` from `itertools` recipes |
| 05 | `itertools.takewhile` |
| 06 | `sliding_window` from `itertools` recipes|
| 07 | iteratively go down a branch and backtrack|
| 08 | `before_and_after` from `itertools` recipes |
| 11 | memory-saving by reducing integer values by taking the modulo of the least common multiple |
| 12 | breadth-first search |
| 13 | recursive walk through a nested list; `functools.cmp_to_key` to sort an iterable by feeding a comparison function; enumerate items from 1 by `enumerate(..., 1)` |
| 14 | `itertools.count`, `__missing__()` class method|
| 15 | yield points on a circle perimeter with `itertools.repeat` and `itertools.accumulate`|
| 16 | Floyd-Warshall algorithm for finding the shortest path length; depth-first search|
| 17 | periodic sequence |
| 18 | breadth-first search to count surface area of an object that has holes|
| 19 | depth-first search and state pruning |
| 20 | indirection |
| 21 | recursion; `sympy` module|
| 22 | a generic solution for folding up a cube net |
| 23 | terminate an iterator by returning `None` |
| 24 | A* algorithm that using Manhattan distance as heuristic |
| 25 | recursively convert between base-10 and base-X integer representation |









