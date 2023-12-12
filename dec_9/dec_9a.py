"""
You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of
many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a
single value. For example:

0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

To best protect the oasis, your environmental report should include a prediction of the next value in each history. To
do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all
zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in
your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first
sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input
sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the
process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information
to extrapolate the history! Visually, these sequences can be arranged like this:

0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0

To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences
between the two values above them, this also means there is now a placeholder in every sequence above it:

0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0

You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to
its left) by 0 (the value below it); this means A must be 3:

0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0

Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below
it), or 18:

0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0

So, the next value of the first history is 18.

Finding all-zero differences for the second history requires an additional sequence:

1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0

Then, following the same process as before, work out the next value in each sequence from the bottom up:

1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0

So, the next value of the second history is 28.

The third history requires even more sequences, but its next value can be found the same way:

10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0

So, the next value of the third history is 68.

If you find the next value for each history in this example and add them together, you get 114.

Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?
"""

from common_functions import load_input


def parse_data_to_ints(data: list[str]) -> list[list[int]]:
    return [list(map(int, row.split())) for row in data]


def get_previous_sequence(sequence: list[int]) -> list[int]:
    return [sequence[i + 1] - sequence[i] for i, _ in enumerate(sequence[0:-1])]


def iterate_over_sequences(sequence: list[int]) -> list[int]:
    history = [sequence]
    print(f"Initial sequence: {sequence}")
    while sum(sequence) != 0:
        sequence = get_previous_sequence(sequence)
        print(f"Iteration: {sequence}")
        history.append(sequence)
    print(f"Histories: {history}")
    return [i[-1] for i in history]


if __name__ == "__main__":
    data = load_input("example.txt")
    print(data)
    data = parse_data_to_ints(data)
    print(data)
    total = 0
    for row in data:
        histories = iterate_over_sequences(row)
        print(histories)
        total += sum(histories)
        print(total)

    print("Part 2!")
    print(f"Initial data: {data}")
    [row.reverse() for row in data]
    print(f"Initial data: {data}")
    total = 0
    for row in data:
        histories = iterate_over_sequences(row)
        print(histories)
        total += sum(histories)
        print(total)
