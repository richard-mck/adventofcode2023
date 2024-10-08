"""
Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.),
mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of
the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it
encounters as it moves:

    If the beam encounters empty space (.), it continues in the same direction.
    If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror.
    For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column,
    while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
    If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the
    splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the
     same direction.
    If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the
    two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a |
    splitter would split into two beams: one that continues upward from the splitter's column and one that continues
    downward from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is
energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in
multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only
showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..

Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the
current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

Part 2
So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward),
any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava,
you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..

Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..

Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that
configuration?
"""

from collections import namedtuple, deque

from common_functions import load_input, transform_data_to_dict_grid, print_grid

Beam = namedtuple("Beam", "pos dir")
Tile = namedtuple("Tile", "type energised direction")

DIRECTIONS = {"right": (0, 1), "down": (1, 0), "left": (0, -1), "up": (-1, 0)}
DIRECTION_SYMBOLS = {(0, 1): ">", (1, 0): "V", (0, -1): "<", (-1, 0): "^"}


def rotate_tuple_clockwise(pos: tuple[int, int]) -> tuple[int, int]:
    """Given a tuple, we can get the next direction clockwise by swapping the values and multiplying right by -1"""
    return pos[1], pos[0] * -1


def rotate_tuple_anticlockwise(pos: tuple[int, int]) -> tuple[int, int]:
    """Given a tuple, we can get the next direction clockwise by swapping the values and multiplying left by -1"""
    return pos[1] * -1, pos[0]


def print_energised_grid(grid: dict, pos: tuple[int, int]):
    grid_to_print = {i: grid[i].type for i in grid}
    grid_to_print[pos] = "*"
    print_grid(grid_to_print)


def print_final_grid(grid: dict):
    grid_to_print = {i: grid[i].direction for i in grid}
    print_grid(grid_to_print)


def compute_next_position(
    position: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    return position[0] + direction[0], position[1] + direction[1]


def compute_next_direction(
    tile_type: str, direction: tuple[int, int]
) -> list[tuple[int, int]]:
    """Given a tile format and a traversal direction, return a list of valid next directions"""
    match tile_type:
        case ".":
            return [direction]
        case "-":
            if direction in [
                DIRECTIONS["left"],
                DIRECTIONS["right"],
            ]:
                return [direction]
            else:
                return [
                    rotate_tuple_clockwise(direction),
                    rotate_tuple_anticlockwise(direction),
                ]
        case "|":
            if direction in [
                DIRECTIONS["up"],
                DIRECTIONS["down"],
            ]:
                return [direction]
            else:
                return [
                    rotate_tuple_clockwise(direction),
                    rotate_tuple_anticlockwise(direction),
                ]
        case "/":
            if direction in [DIRECTIONS["right"], DIRECTIONS["left"]]:
                return [rotate_tuple_anticlockwise(direction)]
            else:
                return [rotate_tuple_clockwise(direction)]
        case "\\":
            if direction in [DIRECTIONS["right"], DIRECTIONS["left"]]:
                return [rotate_tuple_clockwise(direction)]
            else:
                return [rotate_tuple_anticlockwise(direction)]
    return []


def breadth_first_search(grid: dict, beam: Beam) -> dict:
    queue = deque()
    goal = 0
    # Label root node as explored
    grid[beam.pos] = Tile(grid[beam.pos].type, True, DIRECTION_SYMBOLS[beam.dir])
    queue.append(beam)
    splitters = []
    while len(queue) > 0:
        goal += 1
        v = queue.pop()
        if goal >= len(grid) * 2:
            print(f"Probable infinite loop - iteration {goal}")
            return grid
        next_directions = compute_next_direction(grid[v.pos].type, v.dir)
        # No need to check splitters that have already been checked from a given direction
        # e.g. We can tell we have reached a loop in the map if the beam is already in the splitter list
        if len(next_directions) > 1:
            if v not in splitters:
                splitters.append(v)
            else:
                continue
        for direction in next_directions:
            next_pos = compute_next_position(v.pos, direction)
            if next_pos not in grid.keys():
                print(f"Next position doesnt exist -{next_pos}")
                continue
            # Label tiles that have been explored
            new_dir = (
                DIRECTION_SYMBOLS[direction]
                if grid[next_pos].type not in ["/", "\\", "-", "|"]
                else grid[next_pos].type
            )
            grid[next_pos] = Tile(grid[next_pos].type, True, new_dir)
            queue.append(Beam(next_pos, direction))
    return grid


def generate_starting_positions(row_max: int, col_max: int) -> list[tuple]:
    """
    Generate a starting grid - optimisation required
    """
    # 0 1 2 3 4 5 6 7 8 9
    # 1                 9
    # 2                 9
    # 3                 9
    # 4                 9
    # 5                 9
    # 6                 9
    # 7                 9
    # 8                 9
    # 9 1 2 3 4 5 6 7 8 9
    start_bottom = [((0, i), "down") for i in range(col_max)]
    start_top = [((col_max - 1, i), "up") for i in range(col_max)]
    start_right = [((i, 0), "right") for i in range(row_max)]
    start_left = [((i, row_max - 1), "left") for i in range(row_max)]

    return start_left + start_right + start_top + start_bottom


if __name__ == "__main__":
    data = load_input("example.txt")
    grid = transform_data_to_dict_grid(data)
    print_grid(grid)
    beam = Beam((0, 0), (0, 1))
    grid = {i: Tile(grid[i], False, grid[i]) for i in grid}
    print_grid(grid)
    print(grid)
    update_grid = breadth_first_search(grid, beam)
    print_final_grid(update_grid)
    tally = [1 for i in update_grid if update_grid[i].energised]
    print(sum(tally))

    # Part 2
    print("\nPart 2!\n")
    vals = []
    positions = generate_starting_positions(len(data), len(data[0]))
    # Brute force approach - try every possible combination
    for opt in positions:
        grid = transform_data_to_dict_grid(data)
        grid = {i: Tile(grid[i], False, grid[i]) for i in grid}
        beam = Beam(opt[0], DIRECTIONS[opt[1]])
        print_grid(grid)
        print(grid)
        update_grid = breadth_first_search(grid, beam)
        print_final_grid(update_grid)
        tally = [1 for i in update_grid if update_grid[i].energised]
        print(sum(tally))
        vals.append(sum(tally))
    print(vals)
    print(max(vals))
