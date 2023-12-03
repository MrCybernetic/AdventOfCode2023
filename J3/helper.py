def parse_caracters_from_schematics(schematics_path: str) -> list[str]:
    """Parse every caracters from the schematics and return list of unique caracters."""
    unique_caracters = []
    with open(schematics_path, "r") as schematics:
        for line in schematics:
            for caracter in line:
                if caracter not in unique_caracters:
                    unique_caracters.append(caracter)
    return unique_caracters


if __name__ == "__main__":
    print(parse_caracters_from_schematics("J3/puzzle_input.txt"))
