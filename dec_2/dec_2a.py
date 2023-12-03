"""
Example input:
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
Seeking: only 12 red cubes, 13 green cubes, and 14 blue cubes
Result: games 1, 2 and 5

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with
that configuration. However, game 3 would have been impossible because at one point the Elf showed
you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed
 you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.
"""

COLOURS = ["red", "green", "blue"]


def load_input(filename: str) -> list:
    """Given a filename, load the associated file as a list of strings"""
    with open(filename, "r") as f:
        file_content = f.readlines()
    return file_content


def parse_input(input_data: list) -> dict:
    """
    Split a given list into a game dictionary, with the game ID as the key and the rounds as list items for values
    """
    result = {}
    for line in input_data:
        data = line.split(":")
        game_id = data[0].split(" ")[1]
        games = data[1].split(";")
        result[game_id] = games
    return result


def is_round_valid(round: str) -> bool:
    """
    Check if a single round is valid by checking that each colour value is less than the required amount
    :param round: a string containing at least one colour and a digit
    :return: True if the round is valid, False if not
    """
    colour_count = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    for colour in COLOURS:
        index = round.find(colour)
        if index != -1:
            count = int(round[index - 3: index].strip())
            colour_count[colour] -= count
    for item in colour_count:
        if colour_count[item] < 0:
            print(f"Colour: {item} count {colour_count[item]}")
            return False
    return True


if __name__ == "__main__":
    filename = "input_a.txt"
    data = load_input(filename)
    games = parse_input(data)
    game_tally = 0
    for game in games:
        invalid_round = 0
        for round in games[game]:
            if not is_round_valid(round):
                print(f"Invalid round {game}")
                invalid_round += 1
        if invalid_round == 0:
            print(f"Valid game {game}")
            game_tally += int(game)

    print(game_tally)
