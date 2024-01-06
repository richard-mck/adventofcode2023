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


def transpose_data(row_based_data: list[str]) -> list[str]:
    """Given a grid of strings, return the same grid transformed into columns instead of rows"""
    result = []
    for i in range(len(row_based_data[0])):
        temp_list = []
        for j in range(len(row_based_data)):
            temp_list.append(row_based_data[j][i])
        result.append("".join(temp_list))
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


class Tile(object):
    """A single unit within a greater grid"""

    def __init__(self, pos: tuple[int, int], val: str or int):
        self.pos = pos
        self.val = val


class Grid(object):
    """An x/y grid of Tiles or other objects"""

    def __init__(self, raw_data: list[str]):
        self.height = len(raw_data)
        self.width = len(raw_data[0])
        self.grid = {}
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i, j] = raw_data[i][j]

    def inside_grid(self, pos: tuple[int, int]) -> bool:
        (i, j) = pos
        return 0 <= i < self.height and 0 <= j < self.width

    def get_neighbours(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        (i, j) = pos
        all_neighbours = [
            (i, j + 1),  # Right
            (i + 1, j),  # Down
            (i, j - 1),  # Left
            (i - 1, j),  # Up
        ]
        all_neighbours = [k for k in all_neighbours if self.inside_grid(k)]
        return all_neighbours

    def print_grid(self, include_row_nums=False):
        """Given a dictionary grid, print the contents line by line for debugging"""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if include_row_nums and j == 0:
                    print(f"{i}: ", end="")
                if j == self.width - 1:
                    print(self.grid[(i, j)])
                else:
                    print(self.grid[(i, j)], end="")
