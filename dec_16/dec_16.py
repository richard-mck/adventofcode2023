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
    while len(queue) > 0:
        goal += 1
        v = queue.pop()
        if goal >= len(grid) * 2:
            print(f"Probable infinite loop - iteration {goal}")
            return grid
        for direction in compute_next_direction(grid[v.pos].type, v.dir):
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
            if not grid[next_pos].energised:
                grid[next_pos] = Tile(grid[next_pos].type, True, new_dir)
                queue.append(Beam(next_pos, direction))
            elif new_dir in ["/", "\\", "-", "|"]:
                grid[next_pos] = Tile(grid[next_pos].type, True, new_dir)
                queue.append(Beam(next_pos, direction))
            elif grid[v.pos].type == ".":
                grid[next_pos] = Tile(grid[next_pos].type, True, new_dir)
                queue.append(Beam(next_pos, direction))
    return grid


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
