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


# We can iterate over the rows and check for the presence of symbols
def get_indices_of_symbols(row: str) -> list:
    """Given a string, return a list of all non-digit, non-period symbols (stripping whitespace)"""
    row = row.rstrip()
    indices = []
    for index in range(len(row)):
        if row[index] != "." and not row[index].isdigit():
            indices.append(index)
    return indices


# If a symbol is present, we can then check the index, index+1 and index-1 in the current row and the rows
# before and after for numbers
def check_row_for_numbers(digit_dict: dict, symbol_index: int) -> list[int]:
    matched_numbers = []
    for num in digit_dict:
        matches = any(symbol_index - 1 <= i < symbol_index + 1 for i in digit_dict[num])
        if matches:
            matched_numbers.append(num)
    return matched_numbers


def format_numbers_to_indices(row: str) -> dict:
    """
    Given a row, transform it into a dict containing numbers as keys and a list of indices for these numbers as
    values
    """
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
    pass
