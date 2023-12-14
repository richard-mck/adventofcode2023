"""
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The
image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies.
However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the
observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or
columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to
assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each
pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one .
or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations
marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these
lengths?
"""

from collections import namedtuple

from common_functions import load_input

Point = namedtuple("Point", "x y")


def expand_universe(
    raw_data: list[str],
) -> tuple[list[list[str]], list[int], list[int]]:
    modified_data = []
    empty_rows = [i for i in range(len(raw_data)) if "#" not in raw_data[i]]
    for row in raw_data:
        if "#" not in row:
            modified_data.append(list(row))
        modified_data.append(list(row))
    raw_data = modified_data
    transposed_data = [
        [raw_data[j][i] for j in range(len(raw_data))] for i in range(len(raw_data[0]))
    ]
    transposed_data = [
        i for i in range(0, len(transposed_data)) if "#" not in transposed_data[i]
    ]
    empty_cols = transposed_data
    for i in range(len(modified_data)):
        for item in transposed_data:
            modified_data[i].insert(item + transposed_data.index(item), ".")
    return modified_data, empty_rows, empty_cols


def enumerate_galaxies(input_data: list[list[str]]) -> tuple[dict, int]:
    counter = 0
    galaxy_dict = {}
    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if input_data[i][j] == "#":
                counter += 1
                galaxy_dict[counter] = Point(j, i)
    return galaxy_dict, counter


def calculate_distance(galaxy_map: dict, start: int, end: int) -> int:
    dx = abs(galaxy_map[start].x - galaxy_map[end].x)
    dy = abs(galaxy_map[start].y - galaxy_map[end].y)
    print(f"{start} -> {end} distance {dx}x + {dy}y")
    return dx + dy


def get_galactic_distances(galaxy_map: dict, start: int):
    distances = []
    for i in range(1, start + 1):
        for j in range(i, start + 1):
            if i == j:
                continue
            distances.append(calculate_distance(galaxy_map, i, j))
    print(sum(distances))


if __name__ == "__main__":
    filename = "example.txt"
    data = load_input(filename)

    universe, null_rows, null_cols = expand_universe(data)
    print(f"empty rows {null_rows}, empty_cols {null_cols}")
    if filename == "example.txt":
        matched_data = load_input("example_expanded.txt")
        for i in range(len(matched_data)):
            assert matched_data[i] == "".join(universe[i])
        assert len(universe) == 12
        assert len(universe[0]) == 13

    numbered_universe, galaxy_count = enumerate_galaxies(universe)

    get_galactic_distances(numbered_universe, galaxy_count)

    # Part two
    # Recalculate original galaxy positions to set up offset calcs
    second_universe, galaxy_count = enumerate_galaxies(data)
    print(second_universe)
    for item in second_universe:
        print(f"Galaxy: {item} - {second_universe[item]}")
        x_count = [i for i in null_cols if i < second_universe[item].x]

        y_count = [i for i in null_rows if i < second_universe[item].y]
        print(x_count, y_count)
        second_universe[item] = Point(
            second_universe[item].x + 10 * len(x_count),
            second_universe[item].y + 10 * len(y_count),
        )
        print(f"Updated galaxy: {item} - {second_universe[item]}")
    print(galaxy_count)
    print(second_universe)
    get_galactic_distances(second_universe, galaxy_count)
