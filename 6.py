import re
from time import perf_counter

PUZZLE_NUMBER: int = 6

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def read_input() -> list[str]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        return file.read().splitlines()


class Cell:
    def __init__(self, data: str):
        self.__data = data
        self.__path = []
        self.__start = False

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def path(self):
        return self.__path

    def add_path(self, direction: int):
        if direction not in self.__path:
            self.__path.append(direction)

    def is_looping_path(self, direction: int):
        return direction in self.__path

    def __str__(self):
        if self.__start:
            return "^"
        if self.__data == "#":
            return self.__data
        if 5 in self.__path:
            return ("O")
        if any(x in self.__path for x in [0, 2]) and any(x in self.__path for x in [1, 3]):
            return "+"
        if any(x in self.__path for x in [0, 2]):
            return "|"
        if any(x in self.__path for x in [1, 3]):
            return "-"
        else:
            return self.__data


class Map:
    def __init__(self, data: list[str]):
        self.__map = self.__build_map(data)
        self.__original_data = data
        self.__obstacles: list[list[int]] = self.__find_obstacles(data)
        self.__start: tuple[int, int] = self.__find_start(data)
        self.__map[self.__start[1]][self.__start[0]].start = True
        self.__width = len(data[0])
        self.__height = len(data)
        self.__extra_obstacles = 0
        self.__added_obstacle = ()

    def reset_map(self):
        self.__map = self.__build_map(self.__original_data)
        self.__obstacles = self.__find_obstacles(self.__original_data)

    @property
    def added_obstacle(self):
        return self.__added_obstacle

    @staticmethod
    def __build_map(data: list[str]):
        return [[Cell(x) for x in list(row)] for row in data]

    @staticmethod
    def __find_obstacles(data) -> list[list[int]]:
        obstacles: list[list[int]] = []
        for y, row in enumerate(data):
            obstacles.extend([x.start(), y] for x in re.finditer("#", row))
        return obstacles

    @staticmethod
    def __find_start(data) -> tuple[int, int]:
        y: int = [i for i, row in enumerate(data) if "^" in row][0]
        x: int = data[y].index("^")
        return x, y

    @property
    def start_location(self) -> tuple[int, int]:
        return self.__start

    def mark_map(self, location: tuple[int, int], direction: int, data_type: str = "guard") -> None:
        if data_type == "guard":
            self.__map[location[1]][location[0]].data = "X"
            self.__map[location[1]][location[0]].add_path(direction)
        else:
            if 5 not in self.__map[location[1]][location[0]].path and not self.is_obstacle(location):
                self.__map[location[1]][location[0]].add_path(5)
                self.__extra_obstacles += 1
            else:
                print("Already an obstacle there!")

    def is_obstacle(self, position: tuple[int, int]) -> bool:
        return list(position) in self.__obstacles

    def off_the_map(self, position) -> bool:
        return not (0 <= position[0] < self.__width and 0 <= position[1] < self.__height)

    def add_obstacle(self, position):
        self.__obstacles.append(list(position))
        self.__map[position[1]][position[0]].data = "#"
        self.__added_obstacle = position

    @property
    def total_positions(self):
        return sum([x.data for x in row].count("X") for row in self.__map)

    def __str__(self):
        return "\n".join("".join(str(x) for x in row) for row in self.__map)


class Guard:
    def __init__(self, route_map: Map):
        self.__position: tuple[int, int] = route_map.start_location
        self.__map: Map = route_map
        self.__direction: int = UP
        self.__exists: bool = True
        self.__visited = []
        self.__extra_obstacles = []

    def reset_to_start(self):
        self.__position = self.__map.start_location
        self.__direction = UP
        self.__visited = []
        self.__exists = True

    @property
    def exists(self) -> bool:
        return self.__exists

    @property
    def visited(self):
        return self.__visited

    @property
    def extra_obstacles(self):
        return self.__extra_obstacles

    def move(self):
        self.__visited.append((self.__position, self.__direction))
        self.__map.mark_map(self.__position, self.__direction)
        position_in_front = self.get_position_in_front()
        if not self.__map.is_obstacle(position_in_front):
            self.__position = position_in_front
            if self.__map.off_the_map(self.__position):
                self.__exists = False
        else:
            self.__direction = (self.__direction + 1) % 4
        if (self.__position, self.__direction) in self.__visited:
            if self.__map.added_obstacle not in self.__extra_obstacles:
                self.__extra_obstacles.append(self.__map.added_obstacle)
            self.__exists = False

    def get_position_in_front(self):
        if self.__direction == UP:
            return self.__position[0], self.__position[1] - 1
        elif self.__direction == RIGHT:
            return self.__position[0] + 1, self.__position[1]
        elif self.__direction == DOWN:
            return self.__position[0], self.__position[1] + 1
        elif self.__direction == LEFT:
            return self.__position[0] - 1, self.__position[1]


def main():
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()
    start = perf_counter()
    data = read_input()
    route_map = Map(data)
    guard = Guard(route_map)
    while guard.exists:
        guard.move()
    print(f"Part 1: {route_map.total_positions}")
    part1_time = perf_counter()
    print(f"Total time for part 1: {part1_time - start}")
    print()

    path = set([x[0] for x in guard.visited])
    for i, location in enumerate(path):
        route_map.reset_map()
        route_map.add_obstacle(location)
        guard.reset_to_start()
        while guard.exists:
            guard.move()

    print(f"Part 2: {len(guard.extra_obstacles)}")
    part2_time = perf_counter()
    print(f"Total time for part 1: {part2_time - part1_time}")


if __name__ == "__main__":
    main()
