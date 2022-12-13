"""
30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all the other trees between it and an edge of the grid are shorter than it.
Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All the trees around the edge of the grid are visible -
since they are already on the edge, there are no trees to block the view.
In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top.
    (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction;
    for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction;
    for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior,
ßa total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""

from pprint import pprint
import collections
import itertools

tree_tuple = collections.namedtuple('tree_tuple', ['row', 'column', 'height'])
visible_set = set()

with open('day08_input.txt', 'r') as f:
    forest = collections.deque(
        collections.deque(
            tree_tuple(r, c, int(height))
            for c, height in enumerate(line.strip())
        )
        for r, line in enumerate(f.readlines())
    )

top, bottom = forest.popleft(), forest.pop()
visible_set.update(top)
visible_set.update(bottom)
top.pop()
top.popleft()
bottom.popleft()
bottom.pop()
left, right = collections.deque(line.popleft() for line in forest), \
              collections.deque(line.pop() for line in forest)
visible_set.update(left)
visible_set.update(right)
data = sorted(itertools.chain(*forest), key=lambda tree: tree.column)

for edge, row in zip(left, forest):
    highest = edge.height
    for tree in row.copy():
        if tree.height > highest:
            highest = tree.height
            row.remove(tree)
            visible_set.add(tree)

for edge, row in zip(right, forest):
    highest = edge.height
    row_from_right = collections.deque(reversed(row))
    for tree in row_from_right:
        if tree.height > highest:
            highest = tree.height
            row.remove(tree)
            visible_set.add(tree)

forest_rearranged = \
    collections.deque(
        collections.deque(g)
        for _, g in itertools.groupby(data, key=lambda tree: tree.column)
    )

for edge, column in zip(top, forest_rearranged):
    highest = edge.height
    for tree in column.copy():
        if tree.height > highest:
            highest = tree.height
            column.remove(tree)
            visible_set.add(tree)

for edge, column in zip(bottom, forest_rearranged):
    highest = edge.height
    column_from_bottom = collections.deque(reversed(column.copy()))
    for tree in column_from_bottom:
        if tree.height > highest:
            highest = tree.height
            column.remove(tree)
            visible_set.add(tree)

pprint(f'{len(visible_set):,} trees are visible from outside the grid.')  # 1693

"""
To measure the viewing distance from a given tree, look up, down, left, and right from that tree; 
stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. 
(If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; 
the proposed tree house has large eaves to keep it dry, 
so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees 
    (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. 
For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""

tree_tuple = collections.namedtuple('tree_tuple', ['row', 'column', 'height', 'scores'])

with open('day08_input.txt', 'r') as f:
    data = [
        tree_tuple(r, c, int(height), [])
        for r, line in enumerate(f)
        for c, height in enumerate(line.strip())
    ]
    data.sort(key=lambda tree: tree.row)

# score from the left
forest = collections.deque(
    collections.deque(g)
    for _, g in itertools.groupby(data, key=lambda tree: tree.row)
)
data.sort(key=lambda tree: tree.column)
forest_transposed = collections.deque(
    collections.deque(g)
    for _, g in itertools.groupby(
        data,
        key=lambda tree: tree.column
    )
)
nrows, ncols = len(forest) - 1, len(forest_transposed) - 1
fforest = forest.copy()


def score_from_side(direction: str) -> None:
    """Score trees from `direction`"""
    if direction in ('top', 'bottom'):
        def key(t):
            return t.column
    else:
        def key(t):
            return t.row

    data.sort(key=key)
    grid = collections.deque(
        collections.deque(g)
        for _, g in itertools.groupby(data, key=key)
    )

    for line in grid:
        if direction == 'right' or direction == 'bottom':
            line.reverse()
        line_of_sight = collections.deque([line[0]])
        for tree in line:
            if (tree.column == 0) or (tree.column == ncols) or (tree.row == 0) or (tree.row == nrows):
                score = 0
            else:
                score = 0
                for adj in line_of_sight:
                    score += 1
                    if adj.height >= tree.height:
                        break
                line_of_sight.appendleft(tree)
            new_scores = fforest[tree.row][tree.column].scores + [score]
            fforest[tree.row][tree.column] = tree._replace(scores=new_scores)


score_from_side('left')
score_from_side('right')
score_from_side('top')
score_from_side('bottom')
pprint(fforest)


max_score = 1
for tree in itertools.chain(*fforest):
    final = tree.scores[0] * tree.scores[1] * tree.scores[2] * tree.scores[3]
    if final > max_score:
        max_score = final
print(f'The highest visibility score is {max_score}.')
