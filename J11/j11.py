import numpy as np
import matplotlib.pyplot as plt


class Image:
    def __init__(self, file_path):
        self.map = []
        with open(file_path) as file:
            for lines in file:
                self.map.append([])
                for char in lines:
                    if char != "\n":
                        self.map[-1].append(char)

    def expand_space(self, empty_rows_or_columns=2):
        # duplicate every empty row and empty column
        index_of_row_to_duplicate = []
        for index, row in enumerate(self.map):
            if row == ["." for _ in range(len(row))]:
                index_of_row_to_duplicate.append(index)
        index_of_column_to_duplicate = []
        for index, column in enumerate(zip(*self.map)):
            column = list(column)
            if column == ["." for _ in range(len(column))]:
                index_of_column_to_duplicate.append(index)
        for index in reversed(index_of_row_to_duplicate):
            for _ in range(empty_rows_or_columns-1):
                self.map.insert(index, ["." for _ in range(len(self.map[0]))])
        for index in reversed(index_of_column_to_duplicate):
            for _ in range(empty_rows_or_columns-1):
                for row in self.map:
                    row.insert(index, ".")

    def _get_galaxies(self) -> list:
        galaxies = []
        for row_index, row in enumerate(self.map):
            for column_index, char in enumerate(row):
                if char == "#":
                    galaxies.append((row_index, column_index))
        return galaxies

    def __repr__(self) -> str:
        representation = ""
        for row in self.map:
            for char in row:
                if char == "#":
                    representation += "🌑"
                elif char == ".":
                    representation += "⬛"
                else:
                    representation += char
            representation += "\n"
        return representation

    def _get_distance(self, point1: tuple, point2: tuple) -> int:
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def get_sum_of_distances(self) -> int:
        galaxies = self._get_galaxies()
        sum_of_distances = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                sum_of_distances += self._get_distance(galaxies[i], galaxies[j])
        return sum_of_distances


def main():
    # Part 1
    image_test = Image("J11/sample_test.txt")
    image_test.expand_space()
    print(image_test)
    assert (image_test.get_sum_of_distances() == 374)
    image = Image("J11/puzzle_input.txt")
    image.expand_space()
    print(image.get_sum_of_distances())
    # Part 2
    image_test = Image("J11/sample_test.txt")
    image_test.expand_space(100)
    assert (image_test.get_sum_of_distances() == 8410)
    image_test = Image("J11/sample_test.txt")
    image_test.expand_space(10)
    assert (image_test.get_sum_of_distances() == 1030)
    func = []
    image = Image("J11/puzzle_input.txt")
    image.expand_space(10)
    func.append((10, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(20)
    func.append((20, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(30)
    func.append((30, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(40)
    func.append((40, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(50)
    func.append((50, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(100)
    func.append((100, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(200)
    func.append((200, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    image.expand_space(500)
    func.append((500, image.get_sum_of_distances()))
    image = Image("J11/puzzle_input.txt")
    np_func = np.poly1d(np.polyfit([x[0] for x in func], [x[1] for x in func], 2))
    plt.plot([x[0] for x in func], [x[1] for x in func], "o")
    plt.plot([x[0] for x in func], np_func([x[0] for x in func]))
    plt.yscale("log")
    plt.show()
    print(np_func(1000000))


if __name__ == "__main__":
    main()
