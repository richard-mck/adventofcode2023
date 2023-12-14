"""
Reusable functions for loading input and so on
"""


def load_input(filename: str) -> list:
    """Given a filename load it and return its contents as a list, with each item representing a line"""
    with open(filename, "r") as f:
        contents = f.read().split("\n")[:-1]
    return contents
