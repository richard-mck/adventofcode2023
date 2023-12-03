"""
Example input:
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes.
    If any color had even one fewer cube, the game would have been impossible.
    Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
 The power of the minimum set of cubes in game 1 is 48.
 In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?
"""

COLOURS = ["red", "green", "blue"]


def load_input(filename: str) -> list:
    with open(filename, "r") as f:
        file_content = f.readlines()
    return file_content


def parse_input(input_data: list) -> dict:
    result = {}
    for line in input_data:
        data = line.split(":")
        game_id = data[0].split(" ")[1]
        games = data[1].split(";")
        result[game_id] = games
    return result


def count_colours(round: str) -> dict:
    """
    Given a round, tally up the values for each colour
    :param round: a string containing at least one colour and one digit
    :return: a dictionary in the with each colour as keys and the tally of each as values
    """
    colour_count = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for colour in COLOURS:
        index = round.find(colour)
        if index != -1:
            count = int(round[index - 3: index].strip())
            colour_count[colour] += count
    return colour_count


if __name__ == "__main__":
    filename = "input_a.txt"
    data = load_input(filename)
    games = parse_input(data)
    game_power_tally = 0
    for game in games:
        colour_count = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for round in games[game]:
            round_count = count_colours(round)
            for colour in round_count:
                # If a new value is higher than the old one, we can drop the old value
                if round_count[colour] > colour_count[colour]:
                    colour_count[colour] = round_count[colour]
        powers = colour_count["red"] * colour_count["green"] * colour_count["blue"]
        print(f"Round {round} power {powers}")
        game_power_tally += powers

    print(game_power_tally)
