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
def get_indices_of_symbols(row: str) -> list[int]:
    """Given a string, return a list of all * symbols (stripping whitespace)"""
    row = row.rstrip()
    indices = [
        key for key, _ in enumerate(row) if row[key] == "*" and not row[key].isdigit()
    ]
    return indices


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


if __name__ == "__main__":
    data = load_input("example_a.txt")
    # Standard example should yield 4361, 467835
    print(data)
    # TODO: refactor this into proper functions
    symbol_indices = [get_indices_of_symbols(i) for i in data]
    digit_dict = [format_numbers_to_indices(i) for i in data]
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
