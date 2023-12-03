import re


SYMBOLS = ['%', '=', '*', '#', '$', '@', '&', '/', '-', '+']


class PartNumber:
    """A part number from schematics."""

    def __init__(self, schematics_array: list[list[str]], value: int, x: int, y: int):
        self.value = value
        self.x = x
        self.y = y
        self.width = len(str(value))
        self.height = 1
        self.is_symbol_close, self.symbol, self.symbol_coordinates = self.symbol_close(schematics_array)

    def __repr__(self) -> str:
        return f"PartNumber(value: {self.value}, x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, symbol_close: {self.is_symbol_close})"

    def symbol_close(self, schematics_array: list[list[str]]) -> (bool, str):
        """return True if the symbol is close to the part number on the schematic."""
        # check around the part number if there is a symbol
        # if there is a symbol, return True
        # else return False
        number_of_rows = len(schematics_array)
        number_of_columns = len(schematics_array[0])
        for x in range(self.x - 1, self.x + self.width + 1):
            for y in range(self.y - 1, self.y + self.height + 1):
                if (x < 0) or (y < 0) or (x >= number_of_rows) or (y >= number_of_columns):
                    continue
                elif schematics_array[y][x] in SYMBOLS:
                    return True, schematics_array[y][x], (x, y)
        return False, None, None


def schematics_path_to_array(schematics_path: str) -> list[list[str]]:
    """Convert the schematics to an array."""
    schematics_array = []
    with open(schematics_path, "r") as schematics:
        for line in schematics:
            schematics_array.append([])
            for caracter in line:
                if caracter != "\n":
                    schematics_array[-1].append(caracter)
    return schematics_array


def parse_part_numbers_from_schematics(schematics_path: str) -> list[PartNumber]:
    """Parse every part numbers from the schematics and return list of part numbers."""
    part_numbers = []
    with open(schematics_path, "r") as schematics:
        for index, line in enumerate(schematics):
            for match in re.finditer(r"\d+", line):
                part_numbers.append(PartNumber(schematics_path_to_array(schematics_path), int(match.group()), match.start(), index))
    return part_numbers


if __name__ == "__main__":
    part_numbers_on_schematics = parse_part_numbers_from_schematics("J3/puzzle_input.txt")
    # Part 1 : sum of all part numbers whith symbol close to them
    print(sum(part_number.value for part_number in part_numbers_on_schematics if part_number.is_symbol_close))
    # Part 2 : find the gear, calculate the gear ratio and sum them
    potential_gears_on_schematics = [part_number for part_number in part_numbers_on_schematics if part_number.symbol == "*"]
    print(potential_gears_on_schematics)
    # if two gears are close to each other, they are part of the same gear
    gear_ratios = []
    for index, gear in enumerate(potential_gears_on_schematics):
        for other_gear in potential_gears_on_schematics[index + 1:]:
            if (gear.symbol_coordinates[0] == other_gear.symbol_coordinates[0]) and (gear.symbol_coordinates[1] == other_gear.symbol_coordinates[1]):
                gear_ratio = gear.value * other_gear.value
                gear_ratios.append(gear_ratio)
    print(sum(gear_ratios))
