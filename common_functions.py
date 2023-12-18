"""
Reusable functions for loading input and so on
"""


def load_input(filename: str) -> list:
    """Given a filename load it and return its contents as a list, with each item representing a line"""
    with open(filename, "r") as f:
        contents = f.read().split("\n")[:-1]
    return contents


def parse_data_on_empty_rows(raw_data: list[str]) -> list[list[str]]:
    """Given a list of strings demarcated by empty strings, break this into lists and return a list of lists"""
    result = []
    chunk = []
    # Add an extra empty row for consistent handling
    raw_data.append("")
    for row in raw_data:
        if len(row) == 0:
            result.append(chunk)
            chunk = []
            continue
        chunk.append(row)

    return result

def transform_data_to_dict_grid(raw_data: list[str]) -> dict:
    """Given a list of strings, transform this to a dictionary with y/x coordinates as keys"""
    result = {}
    for i in range(len(raw_data)):
        for j in range(len(raw_data[i])):
            result[i, j] = raw_data[i][j]
    return result


def print_grid(grid: dict, include_row_nums=False):
    """Given a dictionary grid, print the contents line by line for debugging"""
    max_y = max(grid.keys())[0]
    max_x = max(grid.keys())[1]
    for i in range(0, max_y + 1):
        for j in range(0, max_x + 1):
            if include_row_nums and j == 0:
                print(f"{i}: ", end="")
            if j == max_x:
                print(grid[(i, j)])
            else:
                print(grid[(i, j)], end="")
