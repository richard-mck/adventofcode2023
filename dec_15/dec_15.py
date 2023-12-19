"""
The HASH algorithm is a way to turn any string of characters into a single number in the range 0 to 255. To run the
HASH algorithm on a string, start with a current value of 0. Then, for each character in the string starting from the
beginning:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.

After following these steps for each character in the string in order, the current value is the output of the HASH
algorithm.

So, to find the result of running the HASH algorithm on the string HASH:

    The current value starts at 0.
    The first character is H; its ASCII code is 72.
    The current value increases to 72.
    The current value is multiplied by 17 to become 1224.
    The current value becomes 200 (the remainder of 1224 divided by 256).
    The next character is A; its ASCII code is 65.
    The current value increases to 265.
    The current value is multiplied by 17 to become 4505.
    The current value becomes 153 (the remainder of 4505 divided by 256).
    The next character is S; its ASCII code is 83.
    The current value increases to 236.
    The current value is multiplied by 17 to become 4012.
    The current value becomes 172 (the remainder of 4012 divided by 256).
    The next character is H; its ASCII code is 72.
    The current value increases to 244.
    The current value is multiplied by 17 to become 4148.
    The current value becomes 52 (the remainder of 4148 divided by 256).

So, the result of running the HASH algorithm on the string HASH is 52.

The initialization sequence (your puzzle input) is a comma-separated list of steps to start the Lava Production
Facility. Ignore newline characters when parsing the initialization sequence. To verify that your HASH algorithm is
working, the book offers the sum of the result of running the HASH algorithm on each step in the initialization
sequence.

For example:

rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7

This initialization sequence specifies 11 individual steps; the result of running the HASH algorithm on each of the
steps is as follows:

    rn=1 becomes 30.
    cm- becomes 253.
    qp=3 becomes 97.
    cm=2 becomes 47.
    qp- becomes 14.
    pc=4 becomes 180.
    ot=9 becomes 9.
    ab=5 becomes 197.
    pc- becomes 48.
    pc=6 becomes 214.
    ot=7 becomes 231.

In this example, the sum of these results is 1320. Unfortunately, the reindeer has stolen the page containing the
expected verification number and is currently running around the facility with it excitedly.

Run the HASH algorithm on each step in the initialization sequence. What is the sum of the results? (The initialization
sequence is one long line; be careful when copy-pasting it.)
"""

from re import search

from common_functions import load_input


def hash_string(unhashed: str) -> int:
    """Given a string, follow the hashing algorithm and return the total value"""
    current = 0
    for char in unhashed:
        # Determine the ASCII code for the current character of the string.
        current += ord(char)
        # Increase the current value by the ASCII code you just determined.
        # Set the current value to itself multiplied by 17.
        current *= 17
        # Set the current value to the remainder of dividing itself by 256.
        current = current % 256
    return current


def parse_data(raw_data: str) -> list[str]:
    return raw_data[0].split(",")


def tally_hashed_list(sequence: list[str]) -> int:
    total = 0
    for item in sequence:
        total += hash_string(item)
    return total


def iterate_on_sequence(unhashed: list[str]) -> dict:
    labels = {i: [] for i in range(0, 256)}
    for item in unhashed:
        key = search("[a-zA-Z]+", item).group()
        action = search("[^a-zA-Z0-9]", item).group()
        index = hash_string(key)
        print(f"{key} - {item} - {action}")
    print(labels)
    return labels
if __name__ == "__main__":
    data = load_input("example.txt")
    print(data)
    data = parse_data(data)
    print(data)
    sequence_sum = tally_hashed_list(data)
    print(sequence_sum)
