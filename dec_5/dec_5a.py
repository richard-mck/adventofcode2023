"""
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use
with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind
of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are
reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into
numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a
seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use
with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire
ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start,
the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line
means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length,
but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds
to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds
to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53
corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil
number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that
needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do
this, you'll need to convert each seed number through other categories until you can find its corresponding location
number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

Part 2:
The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and
the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79
and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values:
55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84,
fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest
location number that corresponds to any of the initial seed numbers?
"""

from common_functions import load_input


class MapRanges(object):
    def __init__(self, destination: int, source: int, range_length: int):
        self.destination = range(destination, destination + range_length)
        self.source = range(source, source + range_length)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(source={self.source!r}, destination={self.destination!r})"


class AlmanacMap(object):
    def __init__(self, name: str, entries: list[str]):
        self.name = name
        self.entries = self.process_entries(entries)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name!r}, entries={self.entries!r})"

    @staticmethod
    def process_entries(entries: list[str]) -> list[MapRanges]:
        result = []
        for item in entries:
            item = [int(i) for i in item.split()]
            result.append(MapRanges(item[0], item[1], item[2]))
        return result


def extract_map_blocks(raw_data: list[str]) -> list[AlmanacMap]:
    result = []
    temp_list = []
    raw_data.append("\n")  # Add a new line to make data consistent
    for row in raw_data:
        if len(row) > 1 and row[0].isalnum():
            temp_list.append(row)
            continue
        result.append(AlmanacMap(temp_list[0], temp_list[1:]))
        temp_list = []

    return result


def convert_source_to_dest_with_map(search_value: int, map_block: AlmanacMap) -> int:
    for entries in map_block.entries:
        if search_value in entries.source:
            return entries.destination[entries.source.index(search_value)]
    return search_value


def get_range_overlap(r1: range, r2: range) -> range or None:
    return (
        range(
            max(r1.start, r2.start),
            min(r1.stop, r2.stop),
        )
        or None
    )


def compare_ranges(r1: range, r2: range, destination: range) -> list[range]:
    # We have 5 possible situations:
    # 1. There is no overlap between seed and source |---Se----|<-------So------> -> Return only seed
    overlap = get_range_overlap(r1, r2)
    if overlap is None:
        return [r1]
    # We can now find the destination indices and convert the overlap:
    start_index = r2.index(overlap.start)
    stop_index = r2.index(overlap.stop - 1)
    overlap = destination[start_index:stop_index]
    result = [overlap]
    # 2. Source overlaps and extends beyond seed |---Se-<---|----So--------> -> Return underlap and matching
    if r1.start < r2.start and r1.stop < r2.stop:
        result.append(range(r1.start, r2[r2.index(r1.stop)]))
    # 3. Seed contains all of source |---Se----<-------So------>---| -> Return underlap, overlap and matching
    if r1.start < r2.start and r1.stop > r2.stop:
        result.append(range(r1.start, r2.start))
        result.append(range(r2.stop, r1.stop))
    # 4. Source starts before seed and extends beyond source <---So---|---Se-->--| -> Return matching and post-match
    if r2.start < r1.start and r1.stop > r2.stop:
        result.append(range(r2.stop, r1.stop))
    # 5. Source is larger in than seed <---|---Se----|---So------> -> Return only matching
    # if r2.start < r1.start and r2.stop > r1.stop:
    #     return [overlap]
    return result


def convert_seeds_to_ranges(raw_seed_nums: list[str]) -> list[range]:
    seed_ranges = []
    while len(raw_seed_nums) != 0:
        seed_ranges.append(
            range(int(raw_seed_nums[0]), int(raw_seed_nums[0]) + int(raw_seed_nums[1]))
        )
        # double pop since the list is updated after the first pop
        raw_seed_nums.pop(0)
        raw_seed_nums.pop(0)
    return seed_ranges


if __name__ == "__main__":
    data = load_input("example.txt")
    seeds = data[0].split()
    map_blocks = extract_map_blocks(data[2:])
    print(map_blocks)
    result = []
    for seed in seeds[1:]:
        seed = int(seed)
        for block in map_blocks:
            seed = convert_source_to_dest_with_map(seed, block)
        result.append(seed)
    print(f"{result} -\n min {min(result)}")
    # Part 2!
    range_of_seeds = convert_seeds_to_ranges(seeds[1:])
    result = []
    for block in map_blocks:
        for entry in block.entries:
            converted_seeds = range_of_seeds
            for seed in converted_seeds:
                next_range = compare_ranges(seed, entry.source, entry.destination)
    print(result)
    pass
