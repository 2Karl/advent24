import re

PUZZLE_NUMBER: int = 6

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def read_input()->list[str]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        return file.read().splitlines()


class Map:
    def __init__(self, data: list[str]):
        self.__map: list[list[str]] = [list(row) for row in data]
        self.__obstacles: list[list[int]] = self.__find_obstacles(data)
        self.__start: tuple[int, int] = self.__find_start(data)
        self.__width = len(data[0])
        self.__height = len(data)
        print(self.__start)

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

    def mark_map(self, location: tuple[int, int]) -> None:
        self.__map[location[1]][location[0]] = "X"

    def is_obstacle(self, position: tuple[int, int]) -> bool:
        return list(position) in self.__obstacles

    def off_the_map(self, position)->bool:
        return not (0 <= position[0] < self.__width and 0 <= position[1] < self.__height)

    @property
    def total_positions(self):
        return sum(row.count("X") for row in self.__map)

    def __str__(self):
        return "\n".join("".join(x for x in row) for row in self.__map)




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
        self.__map.mark_map(self.__position)
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
                self.__exists = False
        else:
            self.__direction = (self.__direction + 1) % 4




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
    data=read_input()
    route_map = Map(data)
    guard = Guard(route_map)
    while guard.exists:
        guard.move()
    print(route_map)
    print(route_map.total_positions)


if __name__ == "__main__":
    main()
