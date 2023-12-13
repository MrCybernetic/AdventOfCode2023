class Pattern:
    def __init__(self, pattern: str):
        self.values = []
        for line in pattern.split('\n'):
            self.values.append([char for char in line if char != '\n'])

    def __str__(self):
        return '\n'.join([''.join(['⬜' if char == '#' else '⬛' for char in line]) for line in self.values])

    def reflection_line(self, old_reflection_line=0):
        horizontal_reflection = 0
        vertical_reflection = 0
        for i in range(1, len(self.values)):
            values_to_mirror = self.values[:i]
            mirrored_values = [value for value in reversed(values_to_mirror)]
            length_to_compare = min(len(mirrored_values), len(self.values[i:]))
            values_to_compare = self.values[i:i+length_to_compare]
            mirrored_values = mirrored_values[:length_to_compare]
            # print("-"*20)
            # print('\n'.join([''.join(['⬜' if char == '#' else '⬛' for char in line]) for line in values_to_compare]))
            # print("-"*20)
            # print('\n'.join([''.join(['⬜' if char == '#' else '⬛' for char in line]) for line in mirrored_values]))
            # print("-"*20)
            if mirrored_values == values_to_compare:
                horizontal_reflection = i

        if horizontal_reflection == 0:
            for i in range(1, len(self.values[0])):
                values_to_mirror = [line[:i] for line in self.values]
                mirrored_values = []
                for line in values_to_mirror:
                    mirrored_values.append([value for value in reversed(line)])
                length_to_compare = min(len(mirrored_values[0]), len(self.values[0][i:]))
                values_to_compare = [line[i:i+length_to_compare] for line in self.values]
                for index, line in enumerate(mirrored_values):
                    mirrored_values[index] = line[:length_to_compare]
                # print("-"*20)
                # print('\n'.join([''.join(['⬜' if char == '#' else '⬛' for char in line]) for line in values_to_compare]))
                # print("-"*20)
                # print('\n'.join([''.join(['⬜' if char == '#' else '⬛' for char in line]) for line in mirrored_values]))
                if mirrored_values == values_to_compare:
                    vertical_reflection = i

        return 100 * horizontal_reflection + vertical_reflection

    def reflection_line_with_smudge_fixed(self):
        old_reflection_line = self.reflection_line()
        for index_row, row in enumerate(self.values):
            for index, char in enumerate(row):
                if char == '#':
                    row[index] = '.'
                else:
                    row[index] = '#'
                self.values[index_row] = row
                new_reflection_line = self.reflection_line()
                if (new_reflection_line != old_reflection_line) and (new_reflection_line != 0):
                    return new_reflection_line
                row[index] = char
                self.values[index_row] = row
        return old_reflection_line


class NoteBook:
    def __init__(self, notebook_path: str):
        self.notes = []
        with open(notebook_path) as notebook:
            for pattern in notebook.read().split('\n\n'):
                self.notes.append(Pattern(pattern))

    def __str__(self):
        return '\n------------------\n'.join([str(note) for note in self.notes])

    def get_sum_of_reflection_lines(self):
        return sum([note.reflection_line() for note in self.notes])

    def get_sum_of_reflection_lines_with_smudge_fixed(self):
        return sum([note.reflection_line_with_smudge_fixed() for note in self.notes])


def main():
    # Part 1
    assert NoteBook('J13/test.txt').get_sum_of_reflection_lines() == 405
    print(NoteBook('J13/input.txt').get_sum_of_reflection_lines())
    # Part 2
    assert NoteBook('J13/test.txt').get_sum_of_reflection_lines_with_smudge_fixed() == 400
    print(NoteBook('J13/input.txt').get_sum_of_reflection_lines_with_smudge_fixed())


if __name__ == '__main__':
    main()
