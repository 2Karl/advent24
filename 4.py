PUZZLE_NUMBER: int = 4


def read_input() -> list[str]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        return [x.strip() for x in file.readlines()]


def vertical_transpose(data) -> list[str]:
    return ["".join(x for x in row) for row in zip(*[list(x) for x in data])]


def diagonal_transpose(data) -> list[str]:
    return ["".join(data[i - j][j] for j in range(i + 1)) for i in range(len(data))] + [
        "".join(data[len(data) - 1 - j][i + j] for j in range(len(data) - i)) for i in range(1, len(data))]


def count_horizontal(data: list[str], search_string: str = "XMAS") -> int:
    return sum(row.count(search_string) + row[::-1].count(search_string) for row in data)


def count_vertical(data: list[str]) -> int:
    return count_horizontal(vertical_transpose(data))


def count_diagonal(data: list[str], search_string: str = "XMAS") -> int:
    return count_horizontal(diagonal_transpose(data), search_string) + count_horizontal(
        diagonal_transpose([x[::-1] for x in data]), search_string)


def count_xmas(data):
    return count_horizontal(data) + count_vertical(data) + count_diagonal(data)


def count_x_mas(data):
    return sum(1 for x in [count_diagonal(square, "MAS") for square in
                           [[data[y + i][x:x + 3] for i in range(3)] for y in range(len(data) - 2) for x in
                            range(len(data) - 2)]] if x == 2)


def main():
    data = read_input()
    print(count_xmas(data))
    print(count_x_mas(data))


if __name__ == "__main__":
    main()
