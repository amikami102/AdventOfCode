"""
Find all of the directories with a total size of at most 100000.
What is the sum of the total sizes of those directories?
"""

with open('day07_input.txt', 'r') as f:
    for line in f:
        if line.startswith('$'):
