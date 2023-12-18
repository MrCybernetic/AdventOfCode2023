from PIL import ImageDraw, Image

dict_digit_to_direction = {
    0: "R",
    1: "D",
    2: "L",
    3: "U"
}


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))


def color_hex_to_int(hex: str) -> int:
    hex = hex.lstrip('#')
    hex = hex[:-1]
    return int(hex, 16)


class DigPlan:
    def __init__(self, plan_path, part: int) -> None:
        self.plane = []
        with open(plan_path, 'r') as f:
            for line in f.readlines():
                if part == 1:
                    self.plane.append(Instruction(line))
        self.image = None

    def dig(self) -> None:
        self.image = Image.new('RGB', (450, 300), color='black')
        pixels = self.image.load()
        digger = (100, 200)
        direction = (0, 0)
        total_cube = 0
        for instruction in self.plane:
            if instruction.direction == "R":
                direction = (1, 0)
            elif instruction.direction == "L":
                direction = (-1, 0)
            elif instruction.direction == "U":
                direction = (0, -1)
            elif instruction.direction == "D":
                direction = (0, 1)
            for i in range(instruction.distance):
                pixels[digger[0] + direction[0] * i, digger[1] + direction[1] * i] = hex_to_rgb(instruction.color)
                total_cube += 1
            digger = (digger[0] + direction[0] * instruction.distance, digger[1] + direction[1] * instruction.distance)

    def fill(self, x, y, color):
        ImageDraw.floodfill(self.image, (x, y), color)

    def count_no_black(self):
        pixels = self.image.load()
        count = 0
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                if pixels[x, y] != (0, 0, 0):
                    count += 1
        return count


class Instruction:
    def __init__(self, line: str) -> None:
        self.direction = line[0]
        self.distance = int(line[1:line.index('(')])
        self.color = line[line.index('(')+1:line.index(')')]


def main():
    # Part 1
    dig_plan_test = DigPlan('J18/test.txt', 1)
    dig_plan_test.dig()
    dig_plan_test.fill(101, 201, (255, 76, 0))
    assert dig_plan_test.count_no_black() == 62
    dig_plan = DigPlan('J18/input.txt', 1)
    dig_plan.dig()
    dig_plan.fill(101, 201, (255, 76, 0))
    dig_plan.image.save('J18/output.png')
    print(dig_plan.count_no_black())


if __name__ == '__main__':
    main()
