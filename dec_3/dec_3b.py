"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is
adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which
gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio
is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because
it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
from re import findall

from common_functions import load_input


# We can iterate over the rows and check for the presence of symbols
def get_indices_of_symbols(raw_data: list[str]) -> dict:
    """Given a string, return a list of all * symbols (stripping whitespace)"""
    result = {}
    for y in range(len(raw_data)):
        for x in range(len(raw_data[y])):
            if raw_data[y][x] == "*":
                result[(x, y)] = raw_data[y][x]
    return result


def format_numbers_to_tuples(raw_data: list[str]) -> dict:
    result = {}
    modified_data = raw_data.copy()
    for y in range(len(modified_data)):
        nums_in_row = [num for num in findall("\d+", raw_data[y])]
        for num in nums_in_row:
            x = modified_data[y].find(num)
            modified_data[y] = modified_data[y].replace(num, "." * len(num), 1)
            result[(x, y)] = raw_data[y][x : x + len(num)]
            for i in range(x, x + len(num)):
                result[(i, y)] = raw_data[y][x : x + len(num)]
    return result


def find_gear_combinations(symbols: dict, nums: dict) -> int:
    # fmt: off
    lookup_table = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0), (0,  0), (1,  0),
        (-1,  1), (0,  1), (1,  1),
    ]
    # fmt: on
    result = 0
    for symbol in symbols:
        x = symbol[0]
        y = symbol[1]
        # Get all positions that have a valid part number
        matches = [
            int(nums[(j[0] + x, j[1] + y)])
            for j in lookup_table
            if (j[0] + x, j[1] + y) in nums.keys()
        ]
        # Extract unique part numbers since the check will find overlaps e.g. [755, 598, 598]
        unique_ratio = list(set(matches))
        print(f"Single pass check {matches}")
        print(f"Unique: {unique_ratio}")
        if len(unique_ratio) > 1:
            result += unique_ratio[0] * unique_ratio[1]
    print(result)
    return result


if __name__ == "__main__":
    data = load_input("example_a.txt")
    # Standard example should yield 4361, 467835
    print(data)
    symbol_indices = get_indices_of_symbols(data)
    digit_dict = format_numbers_to_tuples(data)
    print(f"Symbols {symbol_indices}")
    print(f"Numbers {digit_dict}")
    ratios = find_gear_combinations(symbol_indices, digit_dict)
