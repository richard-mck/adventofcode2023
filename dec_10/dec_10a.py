"""
The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the
    pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large,
continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to
it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes
those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two
neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to
those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting
position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you
need to find the tile that would take the longest number of steps along the loop to reach from the starting point -
regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position
to the point farthest from the starting position?
"""

from collections import namedtuple

from common_functions import load_input

Pipe = namedtuple("Pipe", "valid_next_positions symbol")
Point = namedtuple("Point", "x y")
MapTile = namedtuple("MapTile", "pipe point")

# fmt: off
VALID_PIPES = {
    "|": Pipe(["north", "south"], "│"),  # is a vertical pipe connecting north and south.
    "-": Pipe(["east", "west"], "─"),  # is a horizontal pipe connecting east and west.
    "L": Pipe(["north", "east"], "└"),  # is a 90-degree bend connecting north and east.
    "J": Pipe(["north", "west"], "┘"),  # is a 90-degree bend connecting north and west.
    "7": Pipe(["south", "west"], "┐"),  # is a 90-degree bend connecting south and west.
    "F": Pipe(["south", "east"], "┌"),  # is a 90-degree bend connecting south and east.
    ".": Pipe([], " "),  # is ground; there is no pipe in this tile.
    "S": Pipe(["north", "south", "east", "west"], "S"),  # is the starting position of the animal; there is a pipe on this tile
}
# fmt: on

NEXT_MOVE = {
    "north": Point(0, -1),
    "east": Point(1, 0),
    "south": Point(0, 1),
    "west": Point(-1, 0),
}

DIRECTION_TRANSFORM = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}


def parse_input_data(data: list[str]) -> (list[list[MapTile]], Point):
    pipes = []
    for y in range(len(data)):
        row = []
        for x in range(len(data[y])):
            if data[y][x] == "S":
                start_pos = Point(x, y)
            elif data[y][x] == "\n":
                continue
            row.append(MapTile(VALID_PIPES[data[y][x]], Point(x, y)))
        pipes.append(row)
    return pipes, start_pos


def check_next_position(
    directions: list[str],
    maze: list[list[MapTile]],
    start: Point,
) -> (list[str], list[Point]):
    valid_directions = []
    valid_points = []
    for move in directions:
        direction = DIRECTION_TRANSFORM[move]
        check_tile = maze[start.y + NEXT_MOVE[move].y][start.x + NEXT_MOVE[move].x]
        if direction in check_tile.pipe.valid_next_positions:
            valid_directions.append(move)
            valid_points.append(check_tile)
    return valid_directions, valid_points


def get_next_tiles(
    maze: list[list[MapTile]], curr: MapTile, prev: MapTile
) -> list[MapTile]:
    moves = curr.pipe.valid_next_positions
    next_x_a = curr.point.x + NEXT_MOVE[moves[0]].x
    next_y_a = curr.point.y + NEXT_MOVE[moves[0]].y
    next_tile_a = maze[next_y_a][next_x_a]
    next_x_b = curr.point.x + NEXT_MOVE[moves[1]].x
    next_y_b = curr.point.y + NEXT_MOVE[moves[1]].y
    next_tile_b = maze[next_y_b][next_x_b]
    if next_tile_b == prev:
        return next_tile_a
    else:
        return next_tile_b


def print_maze(current_pos: list[MapTile], maze: list[list[MapTile]], loop_only=False):
    for row in maze:
        for item in row:
            symbol = item.pipe.symbol
            if loop_only and item not in current_pos:
                symbol = " "
            elif not loop_only and item in current_pos:
                symbol = "*"
            if item is row[-1]:
                symbol = symbol + "\n"
            print(symbol, end="")
    print()


if __name__ == "__main__":
    data = load_input("example.txt")
    maze, start = parse_input_data(data)
    start = MapTile(VALID_PIPES["S"], start)
    print(f"Start: {start}")
    moves, tiles = check_next_position(NEXT_MOVE.keys(), maze, start.point)
    print(f"Starting moves: {moves}, starting tiles: {tiles}")
    move = moves[0]
    tile = tiles[0]
    current_tile = tile
    maze_tiles = [start]
    while current_tile != start:
        prev = maze_tiles[-1]
        maze_tiles.append(current_tile)
        current_tile = get_next_tiles(maze, current_tile, prev)
    print_maze(maze_tiles, maze, loop_only=True)
    print(len(maze_tiles) // 2)
    # Part 2
    points = [i.point for i in maze_tiles]
    area = 0
    # Using the shoelace formula - https://en.wikipedia.org/wiki/Shoelace_formula
    # combined with Pick's theorem - https://en.wikipedia.org/wiki/Pick's_theorem
    # Pick's theorem: A = i + (b/2) - 1, where
    #  - A = area = 1/2 ((X1Y2 - X2Y1) + ... + (XnYn+1 - Xn+1Yn))
    #  - i = interior points - what we're solving for
    #  - b = boundary points (e.g. number of loop tiles)
    # Therefore: i = A - (b/2) + 1
    boundary_points = len(points)
    for i in range(0, boundary_points - 1):
        area_n = (points[i].x * points[i + 1].y) - (points[i + 1].x * points[i].y)
        area += area_n
    # For the final point in the matrix, we must consider Xn,Yn and X0,Y0 to complete the boundary
    area += (points[-1].x * points[0].y) - (points[0].x * points[-1].y)
    area = abs(area / 2)
    internal = area - (boundary_points / 2) + 1
    print(f"A:{area}, b:{boundary_points}, i:{internal}")
