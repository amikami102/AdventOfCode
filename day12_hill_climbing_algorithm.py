"""
--- Day 12: Hill Climbing Algorithm ---

"""
from pprint import pprint
import string
import collections
import itertools

alphabet_integer = {letter: i for i, letter in enumerate(string.ascii_lowercase)}
alphabet_integer.update({'S': string.ascii_lowercase.index('a')})
alphabet_integer.update({'E': string.ascii_lowercase.index('z')})


class gridNode:
    """
    A class object holding grid node data. Initialized by feeding row, column, and height attributes.

    Attributes
    ---
        row, column : int, int
            row and column of the node on the map
            the topmost row and the leftmost column have indices 0
        height : int
            the integer value corresponding to the letter of the grid cell
        neighbors : list[gridNode]
            list of other grid nodes that can be reached from this node
        parent : gridNode
            the gridNode from which this node was accessed

    Methods
    ---
        add_neighbor(other)
            adds another gridNode to this node's neighbors list
    """

    def __init__(self, row: int, column: int, height: int):
        self.row, self.column, self.height = row, column, height
        self.neighbors = collections.deque(maxlen=4)
        self.parent = None

    def __repr__(self) -> str:
        return str((self.row, self.column))

    def add_neighbor(self, other):
        self.neighbors.append(other)


class heightMap:
    """
    A class object holding heightmap data. Initialize by feeding the name of the .txt file containing
    heightmap and, optionally, the start node row and column indices as tuple.

    Attributes
    ----
    nodes : list[gridNode]
        list of gridNodes in the graph; each gridNode is represented by a namedtuple
        with attributes row, column, height, and index
    Start : gridNode
        the gridNode representing the start position
    End : gridNode
        the gridNode representing the end position
    path: list[gridNode]
        list of gridNodes tracing the path from Start to End; filled in by bfs()

    Methods
    ----
        determine_adjacency()
            determine node adjacency
        bfs()
            implement Breadth-First Search algorithm
        trace_path()
    """

    def __init__(self, filename: str = 'day12_test.txt') -> None:
        self.nodes = []
        self.Start, self.End = None, None
        self.path = collections.deque()

        with open(filename, 'r') as f:
            for row, line in enumerate(f.readlines()):
                for column, letter in enumerate(line.strip()):
                    v = gridNode(
                        row=row,
                        column=column,
                        height=alphabet_integer[letter]
                    )
                    self.nodes.append(v)
                    if letter == 'E':
                        self.End = v
                    if letter == 'S':
                        self.Start = v

    def determine_adjacency(self) -> None:
        """
        A gridNode is adjacent to another gridNode if
            1) they are on the same row or column,
            2) and the second gridNode's height is at most +1 to the first gridNode's height.
        If the second gridNode is adjacent to the first gridNode,
        add the second gridNode to the first gridNode's neighbors attribute.

        *n.b.* This is a directed graph; adjacency is not necessarily communicative.
        e.g. A node with height 3 can reach a node with height 1. The reverse is not true.
        """

        def iterate_pairwise(horizontal: bool = True):
            """
            Determine adjacency by iterating nodes horizontally if horizontal is True,
            vertically otherwise.
            """
            if horizontal:
                keyfunc = lambda x: x.row
            else:
                keyfunc = lambda x: x.column

            grouped_iterator = itertools.groupby(
                sorted(self.nodes, key=keyfunc),
                keyfunc
            )
            for _, group in grouped_iterator:
                for first, second in itertools.pairwise(group):
                    if second.height - first.height <= 1:
                        first.add_neighbor(second)
                    if first.height - second.height <= 1:
                        second.add_neighbor(first)

        iterate_pairwise(horizontal=True)
        iterate_pairwise(horizontal=False)

    def bfs(self, start: gridNode = None) -> None:
        """
        Implement breadth-first search algorithm to search for a path from Start to End.
        """
        if start is not None:
            self.Start = start
        queue, explored = collections.deque(), []
        queue.clear()
        explored.clear()
        queue.append(self.Start)
        explored.append(self.Start)
        self.Start.parent = None
        while queue:
            v = queue.popleft()
            for neighbor in v.neighbors:
                if neighbor not in explored:
                    explored.append(neighbor)
                    queue.append(neighbor)
                    neighbor.parent = v
            if v == self.End:
                queue.clear()
                explored.clear()
                break

        def trace_path() -> None:
            """
            Trace the predecessors of gridNodes to get the path
            """
            self.path.clear()
            current = self.End
            while current:
                self.path.append(current)
                current = current.parent
            self.path.reverse()

        trace_path()


# part 1
h = heightMap('day12_input.txt')
h.determine_adjacency()
h.bfs()
print(f'The shortest path from Start to End is {len(h.path) - 1} steps long.')

# part 2
h = heightMap('day12_input.txt')
h.determine_adjacency()
starters = (node for node in h.nodes if node.height == 0)
path_lengths = []
for s in starters:
    h.bfs(s)
    path_lengths.append(len(h.path) - 1)
print(f'The shortest path from a to End is {min(path_lengths)} steps long.')

