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
