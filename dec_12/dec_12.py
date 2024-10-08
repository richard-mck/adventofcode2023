"""
In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every
spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself
damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different
format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in
the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the
entire size of its contiguous group (that is, groups are always separated by at least one operational spring: ####
would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For
example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken
springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in
that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken
(#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ?
must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly
one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group
of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#,
there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and
second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run
of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#

In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria.
What is the sum of those counts?
"""

from collections import namedtuple

from common_functions import load_input

SpringGroup = namedtuple("SpringGroup", "condition_log broken_groups")


def parse_group(group: str) -> SpringGroup:
    group = group.split()
    return SpringGroup(group[0], tuple(int(i) for i in group[1].split(",")))


def check_group(conditions: str, group: tuple[int]) -> int:
    """Given a set of conditions and a list of groupings associated with that group,"""
    print(f"Springs {conditions} groups: {group} ", end="")
    char = conditions[0]
    broken_count = group[0]
    print(f"sping: {char} broken: {broken_count}")
    result = 0

    def check_stop():
        """If . we can move immediately on since this doesn't count toward our tally"""
        return check_group(conditions[1:], group)

    def check_hash():
        return 1

    def check_question():
        return check_stop() + check_hash()

    if char == ".":
        result = check_stop()
    elif char == "#":
        result = check_hash()
    elif char == "?":
        result = check_question()

    return result


if __name__ == "__main__":
    data = load_input("example.txt")
    springs = [parse_group(row) for row in data]
    print(springs)
    output = 0
    for row in springs:
        output += check_group(row.condition_log, row.broken_groups)
    print(output)
    pass
