import re


class Document:
    def __init__(self, document_path: str) -> None:
        with open(document_path, "r") as document:
            document_text = document.readlines()
        self.instruction = document_text[0].split('\n')[0]
        self.nodes = self._get_nodes(document_text[2:])

    def _get_nodes(self, lines: list) -> list:
        """
        Return a list of nodes, where each node is a dictionary with the following structure:
        {"L": "node on the left", "R": "node on the right"}
        """
        nodes = {}
        for line in lines:
            line = line.split('\n')[0]
            nodes[line.split()[0]] = {"L": re.findall(r"\((.*),", line)[0], "R": re.findall(r", (.*)\)", line)[0]}
        return nodes

    def get_number_of_steps_to_finish(self) -> int:
        """
        Calculate and return the number of steps required to reach the node "ZZZ"
        starting from the node "AAA", following the instructions in self.instruction.
        """
        number_of_steps_to_finish = 0
        node = "AAA"
        while node != "ZZZ":
            for instruction in self.instruction:
                node = self.nodes[node][instruction]
                number_of_steps_to_finish += 1
                if node == "ZZZ":
                    break
        return number_of_steps_to_finish

    def get_number_of_steps_to_finish_as_ghost(self) -> int:
        """
        Calculate and return the number of steps required for all nodes ending with "A"
        to simultaneously reach a state ending with "Z", following the instructions in self.instruction.
        """
        number_of_steps_to_finish = 0
        current_nodes = self._get_starting_nodes()
        while not all(node[-1] == "Z" for node in current_nodes):
            for instruction in self.instruction:
                current_nodes = [self.nodes[node][instruction] for node in current_nodes]
                number_of_steps_to_finish += 1
                if all(node[-1] == "Z" for node in current_nodes):
                    break
        return number_of_steps_to_finish

    def _get_starting_nodes(self) -> list:
        """Return a list of nodes ending with "A"."""
        starting_nodes = []
        for node in self.nodes:
            if node[-1] == "A":
                starting_nodes.append(node)
        return starting_nodes


def main() -> None:
    input = Document("J8/puzzle_input.txt")
    # Part 1
    print("Part 1:")
    print("  Tests:")
    assert Document("J8/sample_test_1.txt").get_number_of_steps_to_finish() == 2
    print("    -test 1 passed")
    assert Document("J8/sample_test_2.txt").get_number_of_steps_to_finish() == 6
    print("    -test 2 passed")
    print("  Result:")
    print(f"    -> {input.get_number_of_steps_to_finish()}")
    # Part 2
    print("Part 2:")
    print("  Tests:")
    assert Document("J8/sample_test_3.txt").get_number_of_steps_to_finish_as_ghost() == 6
    print("    -test passed")
    print("  Result:")
    print(f"    -> {input.get_number_of_steps_to_finish_as_ghost()}")


if __name__ == "__main__":
    main()
