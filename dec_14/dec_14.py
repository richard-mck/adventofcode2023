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
    updated_puzzle = transpose_data(puzzle)
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
    pprint(transpose_data(return_puzzle))
    return transpose_data(return_puzzle)


if __name__ == "__main__":
    data = load_input("example.txt")
    # We need a function to parse the data into columns then move all the rocks.
    # Rocks can only be moved as far as the first hash they encounter
    print(data)
    moved_rocks = move_rocks_as_strings(data)
    pass
