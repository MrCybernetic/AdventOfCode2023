class Cavern:
    def __init__(self, cavern_path):
        with open(cavern_path) as f:
            self.cavern = [list(line.strip()) for line in f.readlines()]

    def __str__(self):
        string = ""
        for row in self.cavern:
            for char in row:
                if char == "#":
                    string += "🟫"
                elif char == "O":
                    string += "🔴"
                elif char == ".":
                    string += "⬛"
            string += "\n"
        return string

    def lever_part1(self):
        cavern_90 = list(zip(*self.cavern[::-1]))
        # in other direction instead
        cavern_90 = ["".join(row) for row in cavern_90]
        for index, row in enumerate(cavern_90):
            for i in range(len(row)):
                row = row.replace("O.", ".O")
            cavern_90[index] = row
        self.cavern = list(reversed(list(zip(*cavern_90))))

    def lever_part2(self):
        for _ in range(4):
            cavern_90 = list(zip(*self.cavern[::-1]))
            # in other direction instead
            cavern_90 = ["".join(row) for row in cavern_90]
            for index, row in enumerate(cavern_90):
                for _ in range(len(row)):
                    row = row.replace("O.", ".O")
                cavern_90[index] = row
            self.cavern = cavern_90

    def cycle(self, number):
        initial_cavern = self.cavern
        previous_states = {}
        cycle_length = 0
        for i in range(number):
            self.lever_part2()
            state = str(self.cavern)
            if state in previous_states:
                cycle_length = i - previous_states[state]
                break
            else:
                previous_states[state] = i
        cycle_states = list(previous_states.keys())[-cycle_length:]
        self.cavern = initial_cavern
        if cycle_length != 0:
            steps_done = 0
            while str(self.cavern) not in cycle_states:
                self.lever_part2()
                steps_done += 1
            nth_step_in_cycle = cycle_states.index(str(self.cavern))
            number -= steps_done
            number %= cycle_length
            for _ in range(nth_step_in_cycle + number):
                self.lever_part2()
        else:
            for _ in range(number):
                self.lever_part2()

    def get_weight(self):
        return sum([index+1 for index, row in enumerate(reversed(self.cavern)) for char in row if char == "O"])


def main():
    # Part 1
    cavern = Cavern("J14/test.txt")
    cavern.lever_part1()
    assert cavern.get_weight() == 136
    cavern = Cavern("J14/input.txt")
    cavern.lever_part1()
    print(cavern.get_weight())
    # Part 2
    cavern = Cavern("J14/test.txt")
    cavern.cycle(1000000000)
    assert cavern.get_weight() == 64
    cavern = Cavern("J14/input.txt")
    cavern.cycle(1000000000)
    print(cavern.get_weight())


if __name__ == "__main__":
    main()
