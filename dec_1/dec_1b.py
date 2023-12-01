"""
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two,
 three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
['two1nine', 'eightwothree', 'abcone2threexyz', 'xtwone3four', '4nineeightseven2', 'zoneight234', '7pqrstsixteen']

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""


class TrebuchetCalibration(object):
    def __init__(self):
        with open("input.txt", "r") as f:
            self.input_doc = f.readlines()
        self.example = [
            "two1nine",
            "eightwothree",
            "abcone2threexyz",
            "xtwone3four",
            "4nineeightseven2",
            "zoneight234",
            "7pqrstsixteen",
        ]
        self.lookup_table = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]

    def get_nums_from_string(self, line: str) -> str:
        """
        Given a substring, check if it begins with an English word representing a digit
        :param line: an alphanumeric string
        :return: the numeric value of a digit or None if no numbers are present
        """
        for word in self.lookup_table:
            if line.find(word) == 0:
                return str(self.lookup_table.index(word) + 1)
        return None

    def process_line(self, line: str) -> str:
        """
        Iterate over a string to pull out all digits or words representing numbers. Not especially pythonic but makes
        for easier manipulation of raw data.
        :param line: an alphanumeric string containing digits
        :return: the concatenation of the first and last digit in the string, if only one digit is present, it will be
        doubled. e.g. ["7"] becomes "77"
        """
        line_list = [None] * len(line)
        for index in range(len(line)):
            letter = line[index]
            if letter.isdigit():
                line_list[index] = letter
            else:
                line_list[index] = self.get_nums_from_string(line[index:])
        line_list = [i for i in line_list if i is not None]
        return str(line_list[0] + line_list[-1])

    def calculate_values(self, doc: list[str]):
        sum = 0
        for line in doc:
            sum += int(self.process_line(line))
        print(sum)


if __name__ == "__main__":
    treb = TrebuchetCalibration()
    treb.calculate_values(treb.example)
