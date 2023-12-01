"""
each line originally contained a specific calibration value that the Elves now need to recover. On each line, the
calibration value can be found by combining the first digit and the last digit (in that order) to form a single
two-digit number.

For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
"""


class TrebuchetCalibration(object):
    def __init__(self):
        with open("input.txt", "r") as f:
            self.input_doc = f.readlines()

    def calculate_values(self, doc: list[str]) -> int:
        sum = 0
        for line in doc:
            sum_string = ""
            numbers_only = [num for num in line if num.isdigit()]
            sum_string += numbers_only[0]
            sum_string += numbers_only[-1]
            sum += int(sum_string)
        print(sum)


if __name__ == '__main__':
    treb = TrebuchetCalibration()
    treb.calculate_values(treb.input_doc)
