"""
They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:
```
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

In this example, there are three stacks of crates.
Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top.
Stack 2 contains three crates; from bottom to top, they are crates M, C, and D.
Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given.
In each step of the procedure, a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure,
one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1.
Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack;
in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""

import re

initial_stacks, movements = [], []
crate_pattern = re.compile("\[(?P<letter>[A-Z])\]")
move_pattern = re.compile("move (?P<n>[\d]+) from (?P<from>[1-9]) to (?P<to>[1-9])")

# Read the input file and store the initial stack configuration data and movements data separately
with open('day05_input.txt', 'r') as f:
    for line in f:
        if line != '\n':
            initial_stacks.append(line.strip('\n'))
        else:
            break
    for line in f:
        if line != '\n':
            movements.append(line.strip())

# Parse the stacks data
n_stacks = int(initial_stacks.pop().split( )[-1])
stacks = {i + 1: [] for i in range(n_stacks)}
for stack_line in initial_stacks[::-1]:
    stack = stack_line.replace(' '*5, ' [!] ').split(' ')
    for i, crate in enumerate(stack):
        crate_letter = re.match(crate_pattern, crate)
        if crate_letter is not None:
            stacks[i+1].append(crate_letter.group('letter'))

# Parse the movement data and move crates
for move in movements:
    matched = re.match(move_pattern, move)
    n, from_crate, to_crate = \
        int(matched.group('n')), \
        int(matched.group('from')), \
        int(matched.group('to'))
    for _ in range(n):
        crate = stacks[from_crate].pop()
        stacks[to_crate].append(crate)

print(f"The letters on the top of the stacks are {''.join(stack[-1] for stack in stacks.values())}.")

"""
The CrateMover 9001 is notable for many new and exciting features: 
air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
However, the action of moving three crates from stack 1 to stack 3 means 
that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, 
update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. 

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""

# Parse the stacks data
stacks = {i + 1: [] for i in range(n_stacks)}
for stack in initial_stacks[::-1]:
    for i, crate in enumerate(stack.replace(' '*5, ' [!] ').split(' ')):
        crate_letter = re.match(crate_pattern, crate)
        if crate_letter is not None:
            stacks[i+1].append(crate_letter.group('letter'))

# Parse the movement data and move crates
for move in movements:
    matched = re.match(move_pattern, move)
    n, from_crate, to_crate = \
        int(matched.group('n')), \
        int(matched.group('from')), \
        int(matched.group('to'))
    stacks[from_crate], target = stacks[from_crate][:-n], stacks[from_crate][-n:]
    stacks[to_crate].extend(target)

print(f"The letters on the top of the stacks are {''.join(stack[-1] for stack in stacks.values())}.")