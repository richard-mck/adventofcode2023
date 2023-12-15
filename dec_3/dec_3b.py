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


class PartNumber(object):
    def __init__(self, part_number: str):
        self.part_number = part_number
        self.part_int = int(part_number)
        self.indices = []

    def generate_indices(self, index: int):
        self.indices.append(index)
        for i in range(index + 1, index + len(self.part_number)):
            self.indices.append(i)


# We can iterate over the rows and check for the presence of symbols
def get_indices_of_symbols(raw_data: list[str]) -> dict:
    """Given a string, return a list of all * symbols (stripping whitespace)"""
    result = {}
    for y in range(len(raw_data)):
        for x in range(len(raw_data[y])):
            if raw_data[y][x] == "*":
                result[(x, y)] = raw_data[y][x]
    return result


# If a symbol is present, we can then check the index, index+1 and index-1 in the current row and the rows
# before and after for numbers
def check_row_for_numbers(
    part_nums: list[PartNumber], symbol_index: int
) -> list[(int, int)]:
    matched_numbers = []
    for key, value in enumerate(part_nums):
        matches = any(
            symbol_index - 1 <= i <= symbol_index + 1 for i in part_nums[key].indices
        )
        if matches:
            matched_numbers.append((symbol_index, value.part_int))
    return matched_numbers


def format_numbers_to_indices(row: str) -> list[PartNumber]:
    """
    Given a row, transform it into a list of PartNumbers containing numbers as attributes and a list of indices for
    these numbers.
    Replaces checked values in the row as it goes, ensuring no duplicate entries
    """
    result = [PartNumber(num) for num in findall("\d+", row)]
    for item in result:
        index = row.find(item.part_number)
        item.generate_indices(index)
        row = row.replace(item.part_number, "." * len(item.part_number), 1)
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


def find_gear_ratios(rows: list[list[PartNumber]], symbol_index: int) -> list[int]:
    # We have to consider the relationship between a single instance of a symbol and all adjacent rows
    # However, we do not need to consider the relationship between multiple symbols and adjacent rows
    # We can examine our rows symbol by symbol to find matches
    # We know we have a match of two items in a single row if their indices +1 and -1 overlap
    # We know that vertically and diagonally, our number indices must overlap or overlap given +1 and -1
    def multiply_row(row: list):
        return row[0][1] * row[1][1]

    ratios = []
    low = check_row_for_numbers(rows[0], symbol_index)
    med = check_row_for_numbers(rows[1], symbol_index)
    high = check_row_for_numbers(rows[2], symbol_index)
    for item in [low, med, high]:
        if len(item) == 2:
            ratios.append(multiply_row(item))

    return ratios


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
    part_count = []
    for i in range(len(symbol_indices)):
        if len(symbol_indices[i]) == 0:
            continue
        for symbol in symbol_indices[i]:
            ratios = find_gear_ratios(
                [digit_dict[i - 1], digit_dict[i], digit_dict[i + 1]], symbol
            )
            low = check_row_for_numbers(digit_dict[i - 1], symbol)
            med = check_row_for_numbers(digit_dict[i], symbol)
            high = check_row_for_numbers(digit_dict[i + 1], symbol)
            part_count += low + med + high
        print(
            f"Data: {data[i].rstrip()}, symbols: {symbol_indices[i]} - parts: {part_count}"
        )
    print(sum(part_count))
    print(f"Symbols {symbol_indices}")
    print(f"Numbers {digit_dict}")
    ratios = find_gear_combinations(symbol_indices, digit_dict)
