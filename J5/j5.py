import multiprocessing as mp


class Almanac:
    def __init__(self, file_path: str) -> None:
        self.seeds = []
        self.mappings = []
        with open(file_path) as file:
            length_file = len(file.readlines())
            file.seek(0)
            mapping_text_array = []
            for index, line in enumerate(file):
                if index == 0:
                    self.seeds = list(map(int, line.split(":")[1].split()))
                elif index > 1:
                    if line != "\n" and index != length_file-1:
                        mapping_text_array.append(line)
                    elif index == length_file-1:
                        mapping_text_array.append(line)
                        self.mappings.append(Mapping(mapping_text_array))
                        mapping_text_array = []
                    else:
                        self.mappings.append(Mapping(mapping_text_array))
                        mapping_text_array = []

    def __repr__(self) -> str:
        return f"Almanac(seeds: {self.seeds}, mappings: {self.mappings})"

    def get_location_from_seed(self, seed: int) -> int:
        """Return the location from the seed."""
        # seed-to-soil
        soil = self.get_next(seed, "seed", "soil")
        # soil-to-fertilizer
        fertilizer = self.get_next(soil, "soil", "fertilizer")
        # fertilizer-to-water
        water = self.get_next(fertilizer, "fertilizer", "water")
        # water-to-light
        light = self.get_next(water, "water", "light")
        # light-to-temperature
        temperature = self.get_next(light, "light", "temperature")
        # temperature-to-humidity
        humidity = self.get_next(temperature, "temperature", "humidity")
        # humidity-to-location
        return self.get_next(humidity, "humidity", "location")

    def get_next(self, source_value: int, source_name: str, destination_name: str) -> int:
        mapping = next((mapping for mapping in self.mappings if mapping.source == source_name and mapping.destination == destination_name), None)
        if mapping is not None:
            for map in mapping.list_of_maps:
                if source_value >= map["source_range_start"] and source_value < map["source_range_start"] + map["range_length"]:
                    destination_value = map["destination_range_start"] + (source_value - map["source_range_start"])
                    break
                else:
                    destination_value = source_value
            return destination_value
        return None

    def get_min_location(self) -> int:
        """Return the min location."""
        # Create a pool of workers
        with mp.Pool(mp.cpu_count()) as pool:
            # Apply the function to each seed in parallel
            locations = pool.map(self.process_seed, self.seeds)
        # Find the minimum location
        return min(locations)

    def process_seed(self, seed):
        return self.get_location_from_seed(seed)


class Mapping:
    def __init__(self, mapping_text_array: list[str]) -> None:
        self.name = mapping_text_array[0].split(" map:")[0]
        self.source = self.name.split("-to-")[0]
        self.destination = self.name.split("-to-")[1]
        self.list_of_maps = []
        for line in mapping_text_array[1:]:
            line_elements = line.split()
            self.list_of_maps.append({"destination_range_start": int(line_elements[0]), "source_range_start": int(
                line_elements[1]), "range_length": int(line_elements[2])})

    def __repr__(self) -> str:
        return f"Mapping(source: {self.source}, destination: {self.destination}, list_of_maps: {self.list_of_maps})"


def main() -> None:
    # Part 1
    almanac = Almanac("J5/puzzle_input.txt")
    print(almanac.get_min_location())
    # Part 2 -> Failed, have to adopt a different approach -> less CPU and memory intensive
    min_locations = []
    for index, seed in enumerate(almanac.seeds):
        new_seeds = []
        if index % 2 == 0:
            initial_seed = seed
        else:
            range_length = seed
            for i in range(initial_seed, initial_seed+range_length):
                new_seeds.append(i)
            almanac.seeds = new_seeds
            min_locations.append(almanac.get_min_location())
    print(min(min_locations))


if __name__ == "__main__":
    main()
