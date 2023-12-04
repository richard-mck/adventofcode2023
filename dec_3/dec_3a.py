"""
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

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

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58
(middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
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
def get_indices_of_symbols(row: str) -> list:
    """Given a string, return a list of all non-digit, non-period symbols (stripping whitespace)"""
    row = row.rstrip()
    indices = [
        key for key, _ in enumerate(row) if row[key] != "." and not row[key].isdigit()
    ]
    return indices


# If a symbol is present, we can then check the index, index+1 and index-1 in the current row and the rows
# before and after for numbers
def check_row_for_numbers(digit_dict: dict, symbol_index: int) -> list[int]:
    matched_numbers = []
    for num in digit_dict:
        matches = any(
            symbol_index - 1 <= i <= symbol_index + 1 for i in digit_dict[num]
        )
        if matches:
            matched_numbers.append(num)
    return matched_numbers


def format_numbers_to_indices(row: str) -> dict:
    """
    Given a row, transform it into a dict containing numbers as keys and a list of indices for these numbers as
    values
    """
    # TODO: work out how to handle case where a number contains the same digits e.g. 24 contains 4
    # If 24 happens first, the `.find()` function will only grab the first instance
    result = {}
    digit_dict = {
        int(num): [
            index
            for index in range(row.find(num), row.find(num) + len(num))
            if row[index].isdigit() and row[index] in num
        ]
        for num in findall("\d+", row)
    }
    return digit_dict


if __name__ == "__main__":
    data = load_input("example_a.txt")
    print(data)
    # TODO: refactor this into proper functions
    symbol_indices = [get_indices_of_symbols(i) for i in data]
    digit_dict = [format_numbers_to_indices(i) for i in data]
    part_count = []
    for i in range(len(symbol_indices)):
        if len(symbol_indices[i]) == 0:
            continue
        for symbol in symbol_indices[i]:
            low = check_row_for_numbers(digit_dict[i - 1], symbol)
            med = check_row_for_numbers(digit_dict[i], symbol)
            high = check_row_for_numbers(digit_dict[i + 1], symbol)
            part_count += low + med + high
        print(
            f"Data: {data[i].rstrip()}, symbols: {symbol_indices[i]} - parts: {part_count}"
        )
    print(sum(part_count))
