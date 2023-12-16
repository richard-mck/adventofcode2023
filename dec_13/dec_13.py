"""
You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully
analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between
two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns
point at the line between the columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not
perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored;
every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column
3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8,
but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row
7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that,
also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first
pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total
of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your
notes?
"""
from pprint import pprint

from common_functions import load_input, parse_data_on_empty_rows


def transpose_data(row_based_data: list[str]) -> list[str]:
    """Given a grid of strings, return the same grid transformed into columns instead of rows"""
    result = []
    for i in range(len(row_based_data[0])):
        temp_list = []
        for j in range(len(row_based_data)):
            temp_list.append(row_based_data[j][i])
        result.append("".join(temp_list))
    return result


def find_mirrored_rows(puzzle: list[str], row_num_only=False) -> int:
    result = 0
    for i in range(1, len(puzzle)):
        if puzzle[i] == puzzle[i - 1]:
            if row_num_only:
                return i
            puzzle_left = puzzle[: i - 1]
            puzzle_right = puzzle[i + 1 :]
            if len(puzzle_left) == 0 or len(puzzle_right) == 0:
                return 1
            result += find_mirrored_rows(puzzle_left + puzzle_right)
    return result


def print_mirror_with_reflection_line(
    puzzle: list[str], ref_index: int, transpose=False
):
    """Given a mirror and an index, print it out with the mirror line shown"""
    print_str = []
    if transpose:
        puzzle = transpose_data(puzzle)
    for i in range(len(puzzle)):
        if i == ref_index and not transpose:
            print_str.append("-" * len(puzzle[i]) + "\n")
        for j in range(len(puzzle[i])):
            if j == ref_index and transpose:
                print_str.append("|")
            print_str.append(puzzle[i][j])
            if j == len(puzzle[i]) - 1:
                print_str.append("\n")
    print("".join(print_str))


if __name__ == "__main__":
    data = load_input("example.txt")
    puzzles = parse_data_on_empty_rows(data)
    print(puzzles)
    puzzles = [(item, transpose_data(item)) for item in puzzles]
    mirror_sum = 0
    for item in puzzles:
        assert transpose_data(item[0]) == item[1]
        assert item[0] == transpose_data(item[1])
        horizontal = find_mirrored_rows(item[0])
        vertical = find_mirrored_rows(item[1])
        h_row = find_mirrored_rows(item[0], row_num_only=True)
        v_col = find_mirrored_rows(item[1], row_num_only=True)
        if vertical == 1:
            mirror_sum += v_col
            item[1].insert(v_col, "-" * len(item[1][v_col]))
            pprint(item[1])
        elif horizontal == 1:
            mirror_sum += 100 * (h_row)
            item[0].insert(h_row, "-" * len(item[0][h_row]))
            pprint(item[0])
        print(f"Vertical reflection: {vertical}")
        print(f"Horizontal reflection: {horizontal}")
        print(f"Vertical col: {v_col}")
        print(f"Horizontal row: {h_row}")
        print(f"Sum {mirror_sum}")
