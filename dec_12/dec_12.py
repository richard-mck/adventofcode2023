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

from collections import namedtuple, deque

from common_functions import load_input

SpringGroup = namedtuple("SpringGroup", "condition_log broken_groups")


def parse_group(group: str) -> SpringGroup:
    group = group.split()
    return SpringGroup(group[0], tuple(int(i) for i in group[1].split(",")))


def depth_first_search(conditions: str, group: list[int]) -> int:
    """Given a set of possible conditions and known matches, return the total possible combinations"""
    if len(conditions) == 0 and len(group) > 0:
        return 0  # conditions exhausted but there are still groups therefore this path is invalid
    elif len(conditions) == 0 and len(group) == 0:
        return 1  # Conditions exhausted and groups exhausted, this is a valid path
    elif len(conditions) > 0 and len(group) == 0 and "#" not in conditions:
        return 1
    elif len(conditions) > 0 and len(group) == 0 and "#" in conditions:
        return 0
    next_char = conditions[0]
    if next_char == ".":
        result = depth_first_search(conditions[1:], group)
    if next_char == "?":
        # fmt:off
        result = depth_first_search("." + conditions[1:], group) + depth_first_search("#" + conditions[1:], group)
        # fmt:on
    if next_char == "#":
        next_group = group[0]
        condition_block = conditions[:next_group]
        # There must be enough possible conditions left to match the group:
        if len(conditions) < next_group:
            return 0
        # Check that the condition substring is not all stops
        if "." not in condition_block and len(condition_block) == next_group:
            group.pop(0)
            print(f"Match found - {conditions} - {group}")
            result = depth_first_search(conditions[next_group + 1 :], group)
        else:
            result = 0
    # label v as discovered
    # for all directed edges from v to w that are in G.adjacentEdges(v) do
    #     if vertex w is not labeled as discovered then
    #         recursively call DFS(G, w)


def breadth_first_search(conditions: str, group: tuple[int]) -> int:
    """Given a set of possible conditions and known matches, return the total possible combinations"""
    combinations = 0
    index = 0
    group = list(group)
    group_index = 0
    group_count = 0
    hash_nodes = []
    # let Q be a queue
    checked_items = deque()
    # label root as explored
    Checked = namedtuple("Checked", "char position")
    root_node = Checked(conditions[index], index)
    # Q.enqueue(root)
    checked_items.append(root_node)
    # while Q is not empty do
    while len(checked_items) > 0:
        #     v := Q.dequeue()
        vertex = checked_items.pop()
        #     if v is the goal then
        #         return v
        if len(group) == 0:
            return combinations
        if vertex.char == ".":
            index += 1
            checked_items.append(Checked(conditions[index], index))
            continue
        if vertex.char == "?":
            checked_items.append(Checked(".", index))
            checked_items.append(Checked("#", index))
            continue
        if vertex.char == "#":
            hash_nodes.append("#")
            group_count += 1
            if group_count == group[group_index]:
                group_index += 1
            checked_items.append(Checked("#", index))

    #     for all edges from v to w in G.adjacentEdges(v) do
    #         if w is not labeled as explored then
    #             label w as explored
    #             w.parent := v
    #             Q.enqueue(w)


def check_group(conditions: str, groups: list[int]) -> int:
    """Given a set of conditions and a list of groupings associated with that group,"""
    if len(groups) == 0:
        # We have exhausted groups and therefore we may have a valid result
        if "#" not in conditions:
            return 1  # Only . and ? that are . remain
        else:
            return 0  # We haven't counted a necessary #
    if len(conditions) == 0:
        return 0
    char = conditions[0]
    group = groups[0]
    print(f"sping: {char} broken: {group}")

    def check_stop():
        """If . we can move immediately on since this doesn't count toward our tally"""
        return check_group(conditions[1:], groups)

    def check_hash():
        condition_group = conditions[:group]
        if "." in condition_group:
            # We only want conditions that match our possible group
            return 0
        if len(condition_group) == group:
            if len(groups) == 1:
                return 1
            else:
                groups.pop(0)
                return check_group(conditions[group:], groups)
        else:
            return check_group(conditions[group:], groups)

    def check_question():
        return check_stop() + check_hash()

    if char == ".":
        result = check_stop()
    elif char == "#":
        result = check_hash()
    elif char == "?":
        result = check_question()
    # Debugging help
    print(f"{conditions}:{groups} -> {result}")

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
