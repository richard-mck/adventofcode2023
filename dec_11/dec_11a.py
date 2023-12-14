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


def get_empty_row_cols(raw_data: list[str]) -> tuple[list[int], list[int]]:
    empty_rows = [i for i in range(len(raw_data)) if "#" not in raw_data[i]]
    transposed_data = [
        [raw_data[j][i] for j in range(len(raw_data))] for i in range(len(raw_data[0]))
    ]
    empty_cols = [
        i for i in range(0, len(transposed_data)) if "#" not in transposed_data[i]
    ]
    return empty_rows, empty_cols


def enumerate_galaxies(input_data: list[list[str]]) -> tuple[dict, int]:
    counter = 0
    galaxy_dict = {}
    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if input_data[i][j] == "#":
                counter += 1
                galaxy_dict[counter] = Point(j, i)
    return galaxy_dict, counter


def enumerate_galaxies_with_expansion(
    input_data: list[list[str]], empty_rows: list[int], empty_cols: list[int], offset=1
) -> tuple[dict, int]:
    galaxy_counter = 0
    empty_x = 0
    empty_y = 0
    galaxy_dict = {}
    for i in range(len(input_data)):
        if i in empty_rows:
            empty_y += offset
        for j in range(len(input_data[i])):
            if j in empty_cols:
                empty_x += offset
            if input_data[i][j] == "#":
                galaxy_counter += 1
                galaxy_dict[galaxy_counter] = Point(j + empty_x, i + empty_y)
        empty_x = 0
    return galaxy_dict, galaxy_counter


def calculate_distance(galaxy_map: dict, start: int, end: int) -> int:
    dx = abs(galaxy_map[start].x - galaxy_map[end].x)
    dy = abs(galaxy_map[start].y - galaxy_map[end].y)
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

    null_rows, null_cols = get_empty_row_cols(data)
    print(f"empty rows {null_rows}, empty_cols {null_cols}")
    universe, galaxy_count = enumerate_galaxies_with_expansion(
        data, null_rows, null_cols
    )
    get_galactic_distances(universe, galaxy_count)

    # Part two
    print("PART 2!")
    # Recalculate original galaxy positions to set up offset calcs
    test_universe, test_galaxy_count = enumerate_galaxies_with_expansion(
        data, null_rows, null_cols
    )
    get_galactic_distances(test_universe, test_galaxy_count)  # Prints 374 for example
    test_universe, test_galaxy_count = enumerate_galaxies_with_expansion(
        data, null_rows, null_cols, offset=9
    )
    get_galactic_distances(test_universe, test_galaxy_count)  # Prints 1030 for example
    test_universe, test_galaxy_count = enumerate_galaxies_with_expansion(
        data, null_rows, null_cols, offset=99
    )
    get_galactic_distances(test_universe, test_galaxy_count)  # Prints 8410 for example
    test_universe, test_galaxy_count = enumerate_galaxies_with_expansion(
        data, null_rows, null_cols, offset=999999
    )
    get_galactic_distances(
        test_universe, test_galaxy_count
    )  # Prints 82000210 for example
