from multiprocessing import Pool
import PIL.Image as Image

light_hor_img = Image.open("J16/light_horiz.png")
light_ver_img = Image.open("J16/light_verti.png")
mirror1_img = Image.open("J16/mirror1.png")
mirror2_img = Image.open("J16/mirror2.png")
splitter1_img = Image.open("J16/splitter1.png")
splitter2_img = Image.open("J16/splitter2.png")


class Tile:
    def __init__(self, type: str, tile_x: int, tile_y: int):
        self.type = type
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.possible_outputs = []

    def get_possible_outputs(self, from_x: int, from_y: int):
        if self.type == '.':
            self.possible_outputs = [(2 * self.tile_x - from_x, 2 * self.tile_y - from_y)]
        elif self.type == '|':
            if ((self.tile_y == from_y)):
                self.possible_outputs = [(self.tile_x, self.tile_y-1), (self.tile_x, self.tile_y+1)]
            elif (self.tile_x == from_x):
                self.possible_outputs = [(self.tile_x, 2 * self.tile_y - from_y)]
        elif self.type == '-':
            if ((self.tile_y == from_y)):
                self.possible_outputs = [(2 * self.tile_x - from_x, self.tile_y)]
            elif (self.tile_x == from_x):
                self.possible_outputs = [(self.tile_x-1, self.tile_y), (self.tile_x+1, self.tile_y)]
        elif self.type == "/":
            self.possible_outputs = [(self.tile_x - (self.tile_y - from_y), self.tile_y - (self.tile_x - from_x))]
        elif self.type == "\\":
            self.possible_outputs = [(self.tile_x + (self.tile_y - from_y), self.tile_y + (self.tile_x - from_x))]
        else:
            print("Error: unknown tile type")
        return self.possible_outputs


class Cave:
    def __init__(self, cave_path: str) -> None:
        self.path = cave_path
        with open(self.path, 'r') as cave_file:
            cave_lines = cave_file.readlines()
            self.cave = []
            for cave_line in cave_lines:
                self.cave.append([])
                for char in cave_line:
                    if char != '\n':
                        self.cave[-1].append(Tile(char, len(self.cave[-1]), len(self.cave)-1))
        self.energised_tiles = []
        self.energised_tiles_for_vizualizer = []
        self.memory = []
        self.images = []
        self.front_image = self.get_front_image()

    def __str__(self) -> str:
        string = ""
        for cave_line in self.cave:
            for tile in cave_line:
                string += tile.type
            string += "\n"
        return string

    def get_tile(self, x_y: (int, int)) -> Tile:
        return self.cave[x_y[1]][x_y[0]]

    def get_next_possible_tiles(self, x_y: (int, int), from_x_y: (int, int)) -> list:
        if (x_y[0] < 0) or (x_y[1] < 0) or (x_y[0] >= len(self.cave[0])) or (x_y[1] >= len(self.cave)):
            return []
        else:
            possible_outputs = self.get_tile(x_y).get_possible_outputs(from_x_y[0], from_x_y[1])
            if len(possible_outputs) > 0:
                for possible_output in possible_outputs:
                    if (possible_output[0] < 0) or (possible_output[1] < 0) or (possible_output[0] >= len(self.cave[0])) or (possible_output[1] >= len(self.cave)):
                        possible_outputs.remove(possible_output)
                        continue
                return possible_outputs
            else:
                return []

    def turn_light_on(self, start_beam: (int, int), previous_beam: (int, int), vizualizer: bool = False) -> None:
        self.energised_tiles = [start_beam]
        stack = [(start_beam, previous_beam)]
        vizualizer_frame = 0
        while stack:
            beam, previous_beam = stack.pop()
            if (beam, previous_beam) not in self.memory:
                self.memory.append((beam, previous_beam))
                next_beams = self.get_next_possible_tiles(beam, previous_beam)
                for next_beam in next_beams:
                    if next_beam not in self.energised_tiles:
                        self.energised_tiles.append(next_beam)
                        self.energised_tiles_for_vizualizer.append((beam, next_beam))
                        vizualizer_frame += 1
                        if vizualizer and vizualizer_frame % 5 == 0:
                            self.images.append(self.get_image())
                    stack.append((next_beam, beam))
        if vizualizer:
            self.images[0].save('J16/cave.gif', save_all=True, append_images=self.images[1:], optimize=False, duration=20, loop=0)

    def _turn_light_on_recursive(self, beam, previous_beam):
        if (beam, previous_beam) in self.memory:
            return
        else:
            self.memory.append((beam, previous_beam))
            next_beams = self.get_next_possible_tiles(beam, previous_beam)
            for next_beam in next_beams:
                if next_beam not in self.energised_tiles:
                    self.energised_tiles.append(next_beam)
                self._turn_light_on_recursive(next_beam, beam)

    def get_energised_cave(self):
        map_cave = ""
        for cave_line in self.cave:
            for tile in cave_line:
                map_cave += "⬛"
            map_cave += "\n"
        for tile in self.energised_tiles:
            map_cave = map_cave[:tile[1]*(len(self.cave[0])+1)+tile[0]] + "🟨" + map_cave[tile[1]*(len(self.cave[0])+1)+tile[0]+1:]
        return map_cave

    def number_of_energised_tiles(self):
        return len(self.energised_tiles)

    def get_image(self):
        img = Image.new('RGB', (len(self.cave[0])*5, len(self.cave)*5), (0, 0, 0))
        for previous_tile, tile in self.energised_tiles_for_vizualizer:
            if previous_tile[0] == tile[0]:
                img.paste(light_ver_img, (tile[0]*5, tile[1]*5), light_ver_img)
            elif previous_tile[1] == tile[1]:
                img.paste(light_hor_img, (tile[0]*5, tile[1]*5), light_hor_img)
            else:
                img.paste(light_ver_img, (tile[0]*5, tile[1]*5), light_ver_img)
        img.paste(self.front_image, (0, 0), self.front_image)
        return img

    def get_front_image(self) -> Image:
        front_img = Image.new('RGBA', (len(self.cave[0])*5, len(self.cave)*5), (0, 0, 0, 0))
        for y in range(len(self.cave)):
            for x in range(len(self.cave[0])):
                if self.cave[y][x].type == '|':
                    front_img.paste(splitter2_img, (x*5, y*5), splitter2_img)
                elif self.cave[y][x].type == '-':
                    front_img.paste(splitter1_img, (x*5, y*5), splitter1_img)
                elif self.cave[y][x].type == '/':
                    front_img.paste(mirror2_img, (x*5, y*5), mirror2_img)
                elif self.cave[y][x].type == '\\':
                    front_img.paste(mirror1_img, (x*5, y*5), mirror1_img)
        return front_img


def get_max_number_of_energised_tile(cave_path: str):
    cave = Cave(cave_path)
    border_tiles = []
    for x in range(len(cave.cave[0])):
        border_tiles.append([(x, 0), (x, -1)])
        border_tiles.append([(x, len(cave.cave)-1), (x, len(cave.cave))])
    for y in range(len(cave.cave)):
        border_tiles.append([(0, y), (-1, y)])
        border_tiles.append([(len(cave.cave[0])-1, y), (len(cave.cave[0]), y)])

    results = []
    with Pool() as pool:
        for i, result in enumerate(pool.imap_unordered(turn_light_on_for_tile, [(cave_path, border_tile) for border_tile in border_tiles]), 1):
            print(f"Progress: {i}/{len(border_tiles)}")
            results.append(result)

    return max(results)


def turn_light_on_for_tile(args):
    cave_path, border_tile = args
    cave = Cave(cave_path)
    cave.turn_light_on(border_tile[0], border_tile[1])
    return len(cave.energised_tiles)


def main():
    # # Part 1
    # cave_test = Cave("J16/test.txt")
    cave = Cave("J16/input.txt")
    # cave_test.turn_light_on((0, 0), (-1, 0))
    # assert cave_test.number_of_energised_tiles()
    # cave.turn_light_on((0, 0), (-1, 0))
    # print("Part 1:", cave.number_of_energised_tiles())
    # # Part 2
    # assert get_max_number_of_energised_tile(cave_test.path) == 51
    # print("Part 2:", get_max_number_of_energised_tile(cave.path))
    # create vizualizer
    cave.turn_light_on((0, 0), (-1, 0), vizualizer=True)


if __name__ == "__main__":
    main()
