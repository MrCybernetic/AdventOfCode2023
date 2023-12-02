import dataclasses
import re


@dataclasses.dataclass
class Game:
    index: int
    sets: list['SetOfCubes']


@dataclasses.dataclass
class SetOfCubes:
    r: int
    g: int
    b: int


def get_game(line: str) -> Game:
    game_index = re.search(r'Game (\d+)', line).group(1)
    record_text = line.split(':')[1]
    set_of_cubes_text = record_text.split(';')
    sets_of_cubes = []
    for set_text in set_of_cubes_text:
        r_match = re.search(r'(\d+) red', set_text)
        r = int(r_match.group(1)) if r_match else 0
        g_match = re.search(r'(\d+) green', set_text)
        g = int(g_match.group(1)) if g_match else 0
        b_match = re.search(r'(\d+) blue', set_text)
        b = int(b_match.group(1)) if b_match else 0
        set_of_cubes_instance = SetOfCubes(int(r), int(g), int(b))
        sets_of_cubes.append(set_of_cubes_instance)
    return Game(int(game_index), sets_of_cubes)


def read_record(record_path: str) -> list[Game]:
    games = []
    with open(record_path, 'r') as f:
        for line in f:
            games.append(get_game(line))
    return games


def is_game_possible(bag: SetOfCubes, game: Game) -> bool:
    for set_of_cubes in game.sets:
        if set_of_cubes.r > bag.r or set_of_cubes.g > bag.g or set_of_cubes.b > bag.b:
            return False
    return True


def get_power_of_game(game: Game) -> int:
    min_r = max(game.sets, key=lambda x: x.r, default=0).r
    min_g = max(game.sets, key=lambda x: x.g, default=0).g
    min_b = max(game.sets, key=lambda x: x.b, default=0).b
    power = min_r * min_g * min_b
    return power


def part1(record_path: str) -> int:
    bag = SetOfCubes(r=12, g=13, b=14)
    games = read_record(record_path)
    index_possible_games = []
    for game in games:
        if is_game_possible(bag, game):
            index_possible_games.append(game.index)
        else:
            continue
    return sum(index_possible_games)


def part2(record_path: str) -> int:
    games = read_record(record_path)
    power_of_games = []
    for game in games:
        power_of_games.append(get_power_of_game(game))
    return sum(power_of_games)


if __name__ == '__main__':
    print(part1('J2/puzzle_input.txt'))
    print(part2('J2/puzzle_input.txt'))
