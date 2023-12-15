import re
from dataclasses import dataclass


class LineSequencer:
    def __init__(self, line_file_path: str) -> None:
        with open(line_file_path, "r") as f:
            self.steps = f.read().split(",")
        self.boxes = [Box([Lens("", 0)]) for i in range(256)]

    def __str__(self) -> str:
        return str(self.steps)

    def get_sum_of_hash(self) -> int:
        sum = 0
        for step in self.steps:
            hash = get_hash(step)
            sum += hash
        return sum

    def _stick_labels(self) -> None:
        for step in self.steps:
            chars = re.findall(r"[a-z]+", step)[0]
            nth_box = get_hash(chars)
            operation = step.split(chars)[1][0]
            if operation == "-":
                self.boxes[nth_box].lenses = [lens for lens in self.boxes[nth_box].lenses if lens.label != chars]
            elif operation == "=":
                focal_length = int(re.findall(r"\d+", step)[0])
                for lens in self.boxes[nth_box].lenses:
                    if lens.label == chars:
                        lens.focal_length = focal_length
                        break
                else:
                    self.boxes[nth_box].lenses.append(Lens(chars, focal_length))

    def get_focusing_power(self) -> int:
        self._stick_labels()
        power = 0
        for index_box, box in enumerate(self.boxes):
            for index_lens, lens in enumerate(box.lenses):
                power += (index_box + 1) * (index_lens)*lens.focal_length
        return power


@dataclass
class Box:
    lenses: list['Lens']


@dataclass
class Lens:
    label: str
    focal_length: int


def get_hash(string: str) -> int:
    hash = 0
    for char in string:
        ascii_value = ord(char)
        hash += ascii_value
        hash *= 17
        hash = hash % 256
    return hash


def main():
    # Part 1
    assert LineSequencer("J15/test.txt").get_sum_of_hash() == 1320
    print(LineSequencer("J15/input.txt").get_sum_of_hash())
    # Part 2
    assert LineSequencer("J15/test.txt").get_focusing_power() == 145
    print(LineSequencer("J15/input.txt").get_focusing_power())


if __name__ == "__main__":
    main()
