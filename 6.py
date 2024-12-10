import re

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
        return f"data: {self.__data}, path: {self.__path}"


class Map:
    def __init__(self, data: list[str]):
        self.__build_map(data)
        # self.__map: list[list[str]] = [list(row) for row in data]
        self.__map = self.__build_map(data)
        self.__obstacles: list[list[int]] = self.__find_obstacles(data)
        self.__start: tuple[int, int] = self.__find_start(data)
        self.__width = len(data[0])
        self.__height = len(data)
        self.__extra_obstacles = 0
        print(self.__start)

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

    def mark_map(self, location: tuple[int, int], direction:int, data_type:str="guard") -> None:
        if data_type == "guard":
            self.__map[location[1]][location[0]].data = "X"
            self.__map[location[1]][location[0]].add_path(direction)
        else:
            if 5 not in self.__map[location[1]][location[0]].path:
                self.__map[location[1]][location[0]].add_path(5)
                self.__extra_obstacles += 1
            else:
                print("Already an obstacle there!")

    def is_obstacle(self, position: tuple[int, int]) -> bool:
        return list(position) in self.__obstacles

    def off_the_map(self, position) -> bool:
        return not (0 <= position[0] < self.__width and 0 <= position[1] < self.__height)

    @property
    def total_positions(self):
        return sum([x.data for x in row].count("X") for row in self.__map)

    def is_looping_path(self, position: tuple[int, int], direction: int):
        return self.__map[position[1]][position[0]].is_looping_path(direction)

    @property
    def extra_obstacles(self):
        return self.__extra_obstacles

    def __str__(self):
        return "\n".join("".join(str(x) for x in row) for row in self.__map)


class Guard:
    def __init__(self, route_map: Map):
        self.__position: tuple[int, int] = route_map.start_location
        self.__map: Map = route_map
        self.__direction: int = UP
        self.__exists: bool = True



    @property
    def exists(self) -> bool:
        return self.__exists

    def move(self):
        #print(f"move guard {self.__position}, Direction: {self.__direction}")
        self.__map.mark_map(self.__position, self.__direction)
        position_in_front = self.__position
        if self.__direction == UP:
            position_in_front = (self.__position[0], self.__position[1] - 1)
        elif self.__direction == RIGHT:
            position_in_front = (self.__position[0] + 1, self.__position[1])
        elif self.__direction == DOWN:
            position_in_front = (self.__position[0], self.__position[1] + 1)
        elif self.__direction == LEFT:
            position_in_front = (self.__position[0] - 1, self.__position[1])

        if not self.__map.is_obstacle(position_in_front):
            trace = Trace(self.__map, self.__position, self.__direction)
            if trace.enters_loop():
                self.__map.mark_map(position_in_front, self.__direction, data_type="obstacle")
            self.__position = position_in_front
            if self.__map.off_the_map(self.__position):
                self.__exists = False
        else:
            self.__direction = (self.__direction + 1) % 4


class Trace:
    def __init__(self, route_map:Map, start_position: tuple[int,int], start_direction: int):
        self.__map = route_map
        self.__position = start_position
        self.__start_position = start_position
        self.__direction = start_direction


    def enters_loop(self)->bool:
        visited =[(self.__position, self.__direction)]
        self.__direction = (self.__direction+1)%4
        while True:
            visited.append((self.__position, self.__direction))
            #print(f"Trace: {self.__position}, {self.__direction}")
            position_in_front = self.__position
            if self.__direction == UP:
                position_in_front = (self.__position[0], self.__position[1] - 1)
            elif self.__direction == RIGHT:
                position_in_front = (self.__position[0] + 1, self.__position[1])
            elif self.__direction == DOWN:
                position_in_front = (self.__position[0], self.__position[1] + 1)
            elif self.__direction == LEFT:
                position_in_front = (self.__position[0] - 1, self.__position[1])
            if not self.__map.is_obstacle(position_in_front):
                self.__position = position_in_front
                if self.__map.off_the_map(self.__position):
                    return False
            else:
                self.__direction = (self.__direction + 1) % 4

            if (self.__position, self.__direction) in visited or self.__map.is_looping_path(self.__position, self.__direction):
                print(f"Loop created: {self.__start_position}")
                return True




def main():
    data = """....#.....
.........#
..........
..#......#
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()
    data = read_input()
    route_map = Map(data)
    guard = Guard(route_map)
    while guard.exists:
        guard.move()
    print(route_map)
    print(route_map.total_positions)
    print(route_map.extra_obstacles)


if __name__ == "__main__":
    main()
