from queue import PriorityQueue
from dataclasses import dataclass
import math


class CityMap:
    def __init__(self, city_map_path) -> None:
        self.city_map = []
        with open(city_map_path, 'r') as f:
            for y, line in enumerate(f.readlines()):
                self.city_map.append([])
                for x, char in enumerate(line):
                    if char != '\n':
                        self.city_map[y].append(CityBlock((x, y), int(char)))

    def __str__(self) -> str:
        string = ''
        for index_y, line in enumerate(self.city_map):
            for index_x, _ in enumerate(line):
                string += str(self.city_map[index_y][index_x])
            string += '\n'
        return string

    def get_shortest_path_with_max_straight_line(self, start_coord: tuple, end_coord: tuple, max_straight_line: int) -> (list, int):
        start_city_block = self.city_map[start_coord[1]][start_coord[0]]
        end_city_block = self.city_map[end_coord[1]][end_coord[0]]
        start_node = Node(start_city_block)
        end_node = Node(end_city_block)
        visited = set()

        open_list = PriorityQueue()
        open_list.put((start_node.cost, start_node))
        while not open_list.empty():
            _, current_node = open_list.get()

            # Reached end node
            if current_node.actual_city_block.position == end_node.actual_city_block.position:
                path = []
                total_cost = 0
                while current_node is not None:
                    path.append(current_node.actual_city_block.position)
                    total_cost += current_node.actual_city_block.cost
                    current_node = current_node.parent
                # print(start_node.actual_city_block.cost)
                # total_cost -= start_node.actual_city_block.cost
                # print(total_cost)
                return path[::-1], total_cost  # Return reversed path
            else:
                for new_position in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    node_position = (current_node.actual_city_block.position[0] + new_position[0],
                                     current_node.actual_city_block.position[1] + new_position[1])
                    # check if new position is out of bounds
                    if (node_position[1] < 0 or node_position[1] >= len(self.city_map) or node_position[0] < 0 or
                            node_position[0] >= len(self.city_map[0])):
                        continue
                    else:

                        # Create new node
                        new_node = Node(self.city_map[node_position[1]][node_position[0]])
                        new_node.parent = current_node
                        new_node.direction = new_position
                        # Check if new node is in the same direction as the previous node
                        if new_node.direction == current_node.direction:
                            new_node.straight_count = current_node.straight_count + 1
                            # Check if the new node has exceeded the max straight line
                            if new_node.straight_count > max_straight_line:
                                continue
                        else:
                            new_node.straight_count = 0

                        # check if new position is visited
                        if node_position in visited:
                            continue
                        else:
                            visited.add(node_position)

                        new_node.cost = new_node.cost + new_node.parent.cost
                        # Add new node to open list
                        priority = new_node.cost + self.heuristic(new_node.actual_city_block.position, end_node.actual_city_block.position)
                        open_list.put((priority, new_node))

    def heuristic(self, position, end_position):
        return abs(position[0] - end_position[0]) + abs(position[1] - end_position[1])


@dataclass
class CityBlock:
    position: tuple
    cost: int

    def __str__(self) -> str:
        return str(self.cost)


@dataclass
class Node:
    actual_city_block: CityBlock
    parent: 'Node' = None
    direction: tuple = None
    straight_count: int = 0
    cost: int = 0

    def __post_init__(self):
        self.cost = self.actual_city_block.cost

    def __lt__(self, other):
        return self.cost < other.cost


def main():
    # Part 1
    test_city_map = CityMap('J17/test.txt')
    input_city_map = CityMap('J17/input.txt')
    path, cost = test_city_map.get_shortest_path_with_max_straight_line(
        (1, 0), (len(test_city_map.city_map)-1, len(test_city_map.city_map[0])-1), 2)
    print(cost)
    # representation of the path
    for y in range(len(test_city_map.city_map)):
        for x in range(len(test_city_map.city_map[0])):
            if (x, y) in path:
                print('🟥', end='')
            else:
                print('🟧', end='')
        print()
    assert test_city_map.get_shortest_path_with_max_straight_line(
        (0, 0), (len(test_city_map.city_map)-1, len(test_city_map.city_map[0])-1), 2)[1] == 102
    print(input_city_map.get_shortest_path_with_max_straight_line(
        (0, 0), (len(input_city_map.city_map)-1, len(input_city_map.city_map[0])-1), 2)[1])


if __name__ == '__main__':
    main()
