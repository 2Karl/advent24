PUZZLE_NUMBER: int = 1


def read_input() -> tuple[list[int], list[int]]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        data: tuple[list[int], list[int]] = ([], [])
        [[data[x].append(int(row.split()[x])) for x in range(2)] for row in file.readlines()]
        return sorted(data[0]), sorted(data[1])


def main():
    # Part 1
    data = read_input()
    print(sum(abs(data[0][i]-data[1][i]) for i in range(len(data[0]))))

    # Part 2
    print(sum(location_id*data[1].count(location_id) for location_id in data[0]))


if __name__ == "__main__":
    main()
