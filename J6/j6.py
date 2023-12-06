class ResultsReader:
    def __init__(self, file_path: str) -> None:
        self.results = {}
        with open(file_path, "r") as file:
            lines = file.readlines()
            self.results["time"] = [int(time) for time in lines[0].split()[1:]]
            self.results["distance record"] = [int(distance) for distance in lines[1].split()[1:]]
            self.results["time part2"] = [int(lines[0].split("Time:")[1].replace(" ", ""))]
            self.results["distance record part2"] = [int(lines[1].split("Distance:")[1].replace(" ", ""))]

    def __repr__(self) -> str:
        return f"ResultsReader({self.results})"

    def get_all_scores_possible(self, time) -> list:
        possible_scores = []
        for time_spend in range(0, time+1):
            speed = time_spend
            time_left = time - time_spend
            distance = speed * time_left
            possible_scores.append(distance)
        return possible_scores

    def get_number_of_possibilities_to_bet_distance_record(self, times: list[int], distance_records: list[int]) -> int:
        possibilities_list = []
        for index, distance in enumerate(distance_records):
            number_of_possibilities = 0
            for score in self.get_all_scores_possible(times[index]):
                if score > distance:
                    number_of_possibilities += 1
            possibilities_list.append(number_of_possibilities)
        # return the product of all possibilities
        product = 1
        for number in possibilities_list:
            product *= number
        return product


def main():
    # Part 1
    reader = ResultsReader("J6/puzzle_input.txt")
    print(reader.get_number_of_possibilities_to_bet_distance_record(reader.results["time"], reader.results["distance record"]))
    # Part 2
    print(reader.get_number_of_possibilities_to_bet_distance_record(reader.results["time part2"], reader.results["distance record part2"]))


if __name__ == "__main__":
    main()
