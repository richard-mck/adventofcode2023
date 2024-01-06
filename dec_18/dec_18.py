"""
However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle
input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)

The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D),
left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up"
were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the
trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out
from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######

At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next
step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######

Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges
are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava
could it hold?
"""

from common_functions import load_input, print_grid

COMPASS = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


class DigChannel(object):
    def __init__(self, raw_data: str):
        split = raw_data.split()
        self.direction = split[0]
        self.metres = int(split[1])
        self.colour = split[2].replace("(", "").replace(")", "")

    def __repr__(self):
        return f"DigChannel({self.direction}, {self.metres}, {self.colour})"


def dig_trench(instructions: list[DigChannel]) -> dict:
    result = {}
    i = j = 0
    result[(i, j)] = "#"
    for item in instructions:
        if item.direction == "R":
            for x in range(0, item.metres):
                j += 1
                result[(i, j)] = "#"
        elif item.direction == "L":
            for x in range(item.metres, 0, -1):
                j -= 1
                result[(i, j)] = "#"

        elif item.direction == "D":
            for x in range(0, item.metres):
                i += 1
                result[(i, j)] = "#"

        elif item.direction == "U":
            for x in range(item.metres, 0, -1):
                i -= 1
                result[(i, j)] = "#"

    i_max = max(result.keys())[0]
    j_max = max(result.keys())[1]
    print(f"Max i,j {i_max},{j_max}")
    for i in range(0, i_max + 1):
        for j in range(0, j_max + 1):
            if (i, j) not in result.keys():
                result[(i, j)] = "."
    return result


def calculate_area(holes: list[tuple[int, int]]) -> float:
    # Cribbing from day 10:
    # Using the shoelace formula - https://en.wikipedia.org/wiki/Shoelace_formula
    # combined with Pick's theorem - https://en.wikipedia.org/wiki/Pick's_theorem
    # Pick's theorem: A = i + (b/2) - 1, where
    #  - A = area = 1/2 ((X1Y2 - X2Y1) + ... + (XnYn+1 - Xn+1Yn))
    #  - i = interior points - what we're solving for
    #  - b = boundary points (e.g. number of loop tiles)
    # Therefore: i = A - (b/2) + 1
    area = 0
    boundary_points = len(dugout)
    for i in range(0, boundary_points - 1):
        area_n = (dugout[i][1] * dugout[i + 1][0]) - (dugout[i + 1][1] * dugout[i][0])
        area += area_n
    # For the final point in the matrix, we must consider Xn,Yn and X0,Y0 to complete the boundary
    area += (dugout[-1][1] * dugout[0][0]) - (dugout[0][1] * dugout[-1][0])
    area = abs(area / 2)
    internal = area - (boundary_points / 2) + 1
    print(f"A:{area}, b:{boundary_points}, i:{internal}")
    print(f"Sum: {boundary_points + internal}")
    return boundary_points + area


if __name__ == "__main__":
    data = load_input("example.txt")
    print(data)
    channels = [DigChannel(row) for row in data]
    print(channels)
    grid = dig_trench(channels)
    print(grid)
    print_grid(grid)
    dugout = [i for i in grid if grid[i] == "#"]
    print(f"Total channel length: {len(dugout)}")
    area = calculate_area(dugout)

    # Part 2
