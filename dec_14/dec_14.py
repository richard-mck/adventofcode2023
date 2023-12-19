"""
In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets
you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the
cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle
input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't
collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge
of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of
load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
beams?
"""
from pprint import pprint

from common_functions import load_input, transpose_data


def move_rocks_as_strings(puzzle: list[str]) -> list[str]:
    # Assuming initially we are always only moving things north
    # Assuming also that puzzle is unmodified
    updated_puzzle = puzzle.copy()
    return_puzzle = []
    for i in range(len(updated_puzzle)):
        # Find fixed rocks to be reinserted later
        fixed_rocks = [
            j for j in range(len(updated_puzzle[i])) if updated_puzzle[i][j] == "#"
        ]
        # Remove the fixed rocks so we can collapse the mobile rocks within a row
        new_rows = updated_puzzle[i].split("#")
        updated_row = ""
        for row in new_rows:
            rock_count = row.count("O")
            updated_row = (
                updated_row + "O" * rock_count + ("." * (len(row) - rock_count))
            )
        # Reinserted the fixed rocks
        for rock in fixed_rocks:
            updated_row = updated_row[:rock] + "#" + updated_row[rock:]
        return_puzzle.append(updated_row)
    return return_puzzle


def calculate_weight(puzzle: list[str]) -> int:
    total_weight = 0
    for i in range(len(puzzle)):
        rocks = puzzle[i].count("O")
        row_weight = rocks * (len(puzzle) - i)
        total_weight += row_weight
    return total_weight


def cycle_rocks(puzzle: list[str]) -> list[str]:
    # Rotate north:
    north_puzzle = move_rocks_as_strings(transpose_data(puzzle))
    north_puzzle = transpose_data(north_puzzle)
    # print("North")
    # pprint(north_puzzle)

    west_puzzle = move_rocks_as_strings(north_puzzle)
    # print("West")
    # pprint(west_puzzle)

    west_puzzle.reverse()
    south_puzzle = transpose_data(west_puzzle)
    south_puzzle = move_rocks_as_strings(south_puzzle)
    south_puzzle = transpose_data(south_puzzle)
    south_puzzle.reverse()
    # print("South")
    # pprint(south_puzzle)

    east_puzzle = transpose_data(south_puzzle)
    east_puzzle.reverse()
    east_puzzle = transpose_data(east_puzzle)
    east_puzzle = move_rocks_as_strings(east_puzzle)
    east_puzzle = transpose_data(east_puzzle)
    east_puzzle.reverse()
    east_puzzle = transpose_data(east_puzzle)
    # print("East")
    # pprint(east_puzzle)
    return east_puzzle


if __name__ == "__main__":
    data = load_input("example.txt")
    # We need a function to parse the data into columns then move all the rocks.
    # Rocks can only be moved as far as the first hash they encounter
    print(data)
    moved_rocks = move_rocks_as_strings(transpose_data(data))
    calculate_weight(transpose_data(moved_rocks))
    # Part 2
    # We need to figure out what transformations are required for the data to complete a cycle
    # Then we need to work out some sort of simplification so we can do a billion cycles in a reasonable timeframe
    # Naive solution: just run the cycles a billion times
    one_cycle = cycle_rocks(data)
    calculate_weight(one_cycle)
    two_cycle = cycle_rocks(one_cycle)
    three_cycle = cycle_rocks(two_cycle)
    counter = 1000000000
    rocks = data.copy()
    while counter >= 0:
        if counter % 10000 == 0:
            print(counter)
        rocks = cycle_rocks(rocks)
        counter -= 1
    calculate_weight(rocks)
