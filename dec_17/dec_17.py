"""
To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the
crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a
route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and
hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any
particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block.
The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the
bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss
unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most
three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse
direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>

This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive
blocks in the same direction, what is the least heat loss it can incur?
"""

from collections import namedtuple, deque

from common_functions import load_input, Grid

# Block = namedtuple("Block", "pos val visited prior_direction steps_since_turn")
DIRECTIONS = {"right": (0, 1), "down": (1, 0), "left": (0, -1), "up": (-1, 0)}


class Block(object):
    def __init__(
        self,
        pos: tuple[int, int],
        val: int,
        prior_dir: str,
        sslt: int,  # steps since last turn
        heat_loss: int,
    ):
        self.pos = pos
        self.val = val
        self.prior_dir = prior_dir
        self.sslt = sslt
        self.heat_loss = heat_loss

    def __repr__(self):
        return f"Block({self.pos}, {self.val}, {self.prior_dir}, {self.sslt}, {self.heat_loss})"

    def get_neighbours(self):
        (i, j) = self.pos
        return [
            (i + DIRECTIONS["right"][0], j + DIRECTIONS["right"][1]),
            (i + DIRECTIONS["down"][0], j + DIRECTIONS["down"][1]),
            (i + DIRECTIONS["left"][0], j + DIRECTIONS["left"][1]),
            (i + DIRECTIONS["up"][0], j + DIRECTIONS["up"][1]),
        ]

def dijkstra(graph: dict, source: tuple[int, int], destination: tuple[int, int]):
    block_queue = deque()
    dist = {}
    prev = {}
    # Initialise the graph of vertices:
    for item in graph:
        dist[item] = None  # None represents infinity or undefined here
        prev[item] = None
        block_queue.append(Block(item, grid[item], False))
    dist[source] = 0

    # Keep track of the steps since last turn
    steps_taken = 0
    # First moves must be right or down from 0,0 and keep track of prior direction
    prior_dir = ["right", "down"]
    # Search the nearby positions for the lowest possible distance
    while block_queue:
        # Find the blocks in the queue that have the lowest distance to the current block
        block = block_queue.pop()
        # Calculate distance from current block to source
        # Distance is the i,j position of the block multiplied by its weighting
        dist[block.pos] = (block.pos[0] * block.val) + (block.pos[1] * block.val)
        # Maybe useful? https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/dijkstras-algorithm/


if __name__ == "__main__":
    data = load_input("example.txt")
    grid = Grid(data)
    grid.print_grid()
    print(grid.grid)
    # This looks like a breadth first search problem? Or a candidate for A*
    # We know our starting position, and we know our goal
    start = (0, 0)
    goal = (len(data) - 1, len(data[0]) - 1)
    print(f"Start pos {start}:{grid.grid[start]}, goal {goal}:{grid.grid[goal]}")
    # We cannot move more than 3 steps in a single direction, and we can only turn left or right
    # Within those 3 steps, we want the sum of the temperature values to be as low as possible
    # So we likely need a function to sum a path
    # We want to find the route with the lowest "cost" to visit - something to search for
    # This could be a use case for Dijkstra's algorithm? -https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # How do we incorporate the turn requirement into the algorithm? We can treat the heat loss as part of the distance
    # calculation but how does required turning fit?
    # Does this suggest that A* is the more appropriate approach since we can include a heuristic to determine the
    # weight of each move? - https://en.wikipedia.org/wiki/A*_search_algorithm
