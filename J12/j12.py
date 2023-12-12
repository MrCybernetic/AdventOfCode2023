class ConditionRecords:
    def __init__(self, records_path: str):
        self.rows = []
        with open(records_path, 'r') as records_file:
            for line in records_file:
                self.rows.append(Row([condition for condition in line.split(' ')[0]], [int(group_size)
                                 for group_size in line.split(' ')[1].split(',')]))

    def get_sum_of_possible_arrangements(self) -> int:
        sum = 0
        for row in self.rows:
            sum += row.get_number_of_possible_arrangements()
        return sum


class Row:
    def __init__(self, conditions: list, groups: list):
        self.conditions = conditions
        self.groups = groups

    def __repr__(self) -> str:
        return f'conditions: {self.conditions}, groups: {self.groups}'

    def get_number_of_possible_arrangements(self) -> int:
        number_of_possible_arrangements = 0
        number_of_unknowns = self.conditions.count('?')
        number_of_possible_arrangements_max = 2**number_of_unknowns
        for i in range(number_of_possible_arrangements_max):
            binary = bin(i)[2:].zfill(number_of_unknowns)
            arrangement = self.conditions.copy()
            for j in range(len(arrangement)):
                if arrangement[j] == '?':
                    arrangement[j] = '.' if binary[0] == '0' else '#'
                    binary = binary[1:]
            continuous_groups = []
            continuous_groups_count = 0
            for condition in arrangement:
                if condition == '#':
                    continuous_groups_count += 1
                else:
                    if continuous_groups_count != 0:
                        continuous_groups.append(continuous_groups_count)
                    continuous_groups_count = 0
            if continuous_groups_count != 0:
                continuous_groups.append(continuous_groups_count)
            if continuous_groups == self.groups:
                number_of_possible_arrangements += 1
        return number_of_possible_arrangements


def main():
    assert ConditionRecords('J12/example.txt').get_sum_of_possible_arrangements() == 21
    print(ConditionRecords('J12/input.txt').get_sum_of_possible_arrangements())


if __name__ == '__main__':
    main()
