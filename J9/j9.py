class Report:
    def __init__(self, report_path: str) -> None:
        self.dataset = []
        with open(report_path) as report_file:
            for line in report_file:
                self.dataset.append(History(line.split("\n")[0]))

    def get_sum_of_last_value(self) -> int:
        return sum([history.all_sequences_with_prediction[0][-1] for history in self.dataset])

    def get_sum_of_first_value(self) -> int:
        return sum([history.all_sequences_with_prediction[0][0] for history in self.dataset])


class History:
    def __init__(self, history: str) -> None:
        self.value = [int(data) for data in history.split()]
        self.all_sequences = self._get_all_sequences(self.value)
        self.all_sequences_with_prediction = self._get_all_sequences_with_prediction()

    def __repr__(self) -> str:
        return str(self.value)

    def _get_next_sequence(self, sequence: list) -> list:
        next_sequence = [sequence[i + 1] - sequence[i] for i in range(0, len(sequence)-1)]
        return next_sequence

    def _get_all_sequences(self, sequence: list) -> list:
        all_sequences = [sequence]
        while not all_sequences[-1] == [0] * len(all_sequences[-1]):
            all_sequences.append(self._get_next_sequence(all_sequences[-1]))
        return all_sequences

    def _get_all_sequences_with_prediction(self) -> list:
        all_sequences_with_prediction = self.all_sequences.copy()
        for index, sequence in enumerate(self.all_sequences):
            if index == 0:
                all_sequences_with_prediction[len(self.all_sequences) - 1].append(0)
                # for part 2
                all_sequences_with_prediction[len(self.all_sequences) - 1].insert(0, 0)
            else:
                all_sequences_with_prediction[len(self.all_sequences) - index - 1].append(
                    all_sequences_with_prediction[len(self.all_sequences) - index][-1]
                    + all_sequences_with_prediction[len(self.all_sequences) - index - 1][-1]
                )
                # for part 2
                all_sequences_with_prediction[len(self.all_sequences) - index - 1].insert(
                    0,
                    all_sequences_with_prediction[len(self.all_sequences) - index - 1][0]
                    - all_sequences_with_prediction[len(self.all_sequences) - index][0]
                )

        return all_sequences_with_prediction


def main():
    # Part 1
    assert (Report("j9/sample_test.txt").get_sum_of_last_value() == 114)
    print(Report("j9/puzzle_input.txt").get_sum_of_last_value())
    # Part 2
    assert (Report("j9/sample_test.txt").get_sum_of_first_value() == 2)
    print(Report("j9/puzzle_input.txt").get_sum_of_first_value())


if __name__ == "__main__":
    main()
