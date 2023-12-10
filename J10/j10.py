from PIL import Image, ImageDraw

TILES = {"|": "vertical_pipe.png", "-": "horizontal_pipe.png", "L": "north_east.png",
         "J": "north_west.png", "7": "south_west.png", "F": "south_east.png", ".": "ground.png",
         "S": "start.png"}
TILE_WIDTH = 6
TILE_HEIGHT = 6


class Map:
    def __init__(self, file_path: str) -> None:
        self.map = []
        with open(file_path) as map_file:
            for line in map_file:
                self.map.append([])
                for char in line:
                    if char == "\n":
                        continue
                    self.map[-1].append(char)
        self.path = file_path
        self.image = self.create_map_image(self.path[:-4] + ".png")

    def __repr__(self) -> str:
        string = ""
        for row in self.map:
            string += "".join(row) + "\n"
        return string

    def _get_tile(self, x: int, y: int) -> str:
        return self.map[y][x]

    def _get_tile_image(self, x: int, y: int) -> str:
        return TILES[self._get_tile(x, y)]

    def _get_tile_image_path(self, x: int, y: int) -> str:
        return "J10/tiles/" + self._get_tile_image(x, y)

    def create_map_image(self, path: str) -> None:
        image = Image.new("RGB", (len(self.map[0])*TILE_WIDTH, len(self.map)*TILE_HEIGHT), (0, 255, 0))
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                tile_path = self._get_tile_image_path(x, y)
                tile_img = Image.open(tile_path)
                image.paste(tile_img, (x*TILE_WIDTH, y*TILE_HEIGHT))
        return image

    def get_max_distance_from_start(self, gif_generate: bool = False) -> int:
        return self.looking_both_ways(gif_generate)[0]

    def looking_both_ways(self, gif_generate: bool = False) -> (int, list):
        start_pos = self._get_start_pos()
        dict_map = self._get_dict_map()
        two_way = self.get_first_pos_in_both_directions(start_pos, dict_map)
        player1_pos = two_way[0]
        player2_pos = two_way[1]
        previous_pos1 = start_pos
        previous_pos2 = start_pos
        distance = 0
        pos_already_visited = [start_pos, player1_pos, player2_pos]
        images = []
        image_count = 0
        while player1_pos != player2_pos:
            if gif_generate:
                if image_count % 3 == 0:
                    images.append(self.generate_gif_frame(player1_pos, player2_pos))
                image_count += 1
            next_pos1 = self.get_next_pos(previous_pos1, player1_pos, dict_map)
            next_pos2 = self.get_next_pos(previous_pos2, player2_pos, dict_map)
            distance += 1
            previous_pos1 = player1_pos
            previous_pos2 = player2_pos
            player1_pos = next_pos1
            player2_pos = next_pos2
            pos_already_visited.append(player1_pos)
            pos_already_visited.append(player2_pos)
        return distance+1, pos_already_visited

    def get_first_pos_in_both_directions(self, start_pos: (int, int), dict_map: dict) -> list:
        two_way = []
        # north
        if self.is_connected(start_pos, (start_pos[0], start_pos[1]-1), dict_map):
            two_way.append((start_pos[0], start_pos[1]-1))
        # east
        if self.is_connected(start_pos, (start_pos[0]+1, start_pos[1]), dict_map):
            two_way.append((start_pos[0]+1, start_pos[1]))
        # south
        if self.is_connected(start_pos, (start_pos[0], start_pos[1]+1), dict_map):
            two_way.append((start_pos[0], start_pos[1]+1))
        # west
        if self.is_connected(start_pos, (start_pos[0]-1, start_pos[1]), dict_map):
            two_way.append((start_pos[0]-1, start_pos[1]))
        return two_way

    def generate_gif_frame(self, pos1: (int, int), pos2: (int, int)) -> list:
        pos1_path = "J10/tiles/player1.png"
        pos2_path = "J10/tiles/player2.png"
        image = Image.open(self.path[:-4] + ".png")
        pos1_img = Image.open(pos1_path)
        pos2_img = Image.open(pos2_path)
        image.paste(pos1_img, (pos1[0]*TILE_WIDTH, pos1[1]*TILE_HEIGHT))
        image.paste(pos2_img, (pos2[0]*TILE_WIDTH, pos2[1]*TILE_HEIGHT))
        return image

    def generate_gif(self, images: list) -> None:
        print("Generating gif...")
        images[0].save(self.path[:-4] + ".gif", save_all=True, append_images=images[1:], duration=1, loop=0, optimize=True)
        print("Gif generated")
        return None

    def get_next_possible_pos(self, pos: (int, int), dict_map: dict) -> list:
        if pos not in dict_map:
            return []
        else:
            return dict_map[pos]

    def get_next_pos(self, previous_pos: (int, int), current_pos: (int, int), dict_map: dict) -> (int, int):
        next_possible_pos = self.get_next_possible_pos(current_pos, dict_map)
        return next_possible_pos[0] if previous_pos != next_possible_pos[0] else next_possible_pos[1]

    def is_connected(self, pos_1: (int, int), pos_2: (int, int), dict_map: dict) -> bool:
        next_possible_pos1 = self.get_next_possible_pos(pos_1, dict_map)
        next_possible_pos2 = self.get_next_possible_pos(pos_2, dict_map)
        return pos_1 in next_possible_pos2 and pos_2 in next_possible_pos1

    def _get_start_pos(self) -> (int, int):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self._get_tile(x, y) == "S":
                    return x, y
        return None

    def _get_dict_map(self) -> dict:
        dict_map = {}
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self._get_tile(x, y) == "S":
                    dict_map[(x, y)] = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
                elif self._get_tile(x, y) == "|":
                    dict_map[(x, y)] = [(x, y-1), (x, y+1)]
                elif self._get_tile(x, y) == "-":
                    dict_map[(x, y)] = [(x-1, y), (x+1, y)]
                elif self._get_tile(x, y) == "L":
                    dict_map[(x, y)] = [(x+1, y), (x, y-1)]
                elif self._get_tile(x, y) == "J":
                    dict_map[(x, y)] = [(x-1, y), (x, y-1)]
                elif self._get_tile(x, y) == "7":
                    dict_map[(x, y)] = [(x-1, y), (x, y+1)]
                elif self._get_tile(x, y) == "F":
                    dict_map[(x, y)] = [(x+1, y), (x, y+1)]
                elif self._get_tile(x, y) == ".":
                    dict_map[(x, y)] = []
        return dict_map

    def get_image_filled(self, image, coords, color) -> Image:
        image_flooded = image.copy()
        ImageDraw.floodfill(image_flooded, xy=coords, value=color)
        return image_flooded

    def get_first_player1_pos(self) -> (int, int):
        return self.looking_both_ways()[1][3]

    def get_number_of_tiles_for_part2(self) -> int:
        spot_path = "J10/tiles/spot.png"
        spot_img = Image.open(spot_path)
        blue = (0, 0, 255)
        image = self.get_image_filled(self.image, (1, 1), blue)
        player1_pos_scaled = (self.get_first_player1_pos()[0]*TILE_WIDTH+TILE_WIDTH/2,
                              self.get_first_player1_pos()[1]*TILE_HEIGHT+TILE_HEIGHT/2)
        image = self.get_image_filled(image, player1_pos_scaled, blue)
        count = 0
        for y in range(0, len(self.map)*TILE_HEIGHT, TILE_HEIGHT):
            for x in range(0, len(self.map[0])*TILE_WIDTH, TILE_WIDTH):
                is_blue = False
                for pixel_y in range(y, y+TILE_HEIGHT):
                    for pixel_x in range(x, x+TILE_WIDTH):
                        if image.getpixel((pixel_x, pixel_y)) == blue:
                            is_blue = True
                if not (is_blue):
                    image.paste(spot_img, (x, y))
                    count += 1
        image.save(self.path[:-4]+"_part2"+".png")
        # remove the start tile
        count = count-1
        return count


def main():
    map_test_1 = Map("J10/sample_test_1.txt")
    map_test_2 = Map("J10/sample_test_2.txt")
    map_test_3 = Map("J10/sample_test_3.txt")
    map_puzzle_input = Map("J10/puzzle_input.txt")
    # Part1
    assert (map_test_1.get_max_distance_from_start() == 4)
    assert (map_test_2.get_max_distance_from_start() == 8)
    print(map_puzzle_input.get_max_distance_from_start())
    # print(map_puzzle_input.get_max_distance_from_start(gif_generate=True))
    # Part2
    assert (map_test_3.get_number_of_tiles_for_part2() == 10)
    print(map_puzzle_input.get_number_of_tiles_for_part2())


if __name__ == "__main__":
    main()
