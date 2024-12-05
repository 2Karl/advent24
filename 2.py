PUZZLE_NUMBER: int = 2


def read_input() -> list[list[int]]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        return [[int(x) for x in row.split()] for row in file.readlines()]


def is_safe(report: list[int]) -> bool:
    diff: list[int] = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    return all(0 < x < 4 for x in diff) or all(-4 < x < 0 for x in diff)


def main():
    data = read_input()
    safe_count: int = 0
    for report in data:
        if is_safe(report):
            safe_count += 1
        else:
            for i in range(len(report)):
                if is_safe(report[:i] + report[i + 1:]):
                    safe_count += 1
                    break
    print(safe_count)


if __name__ == "__main__":
    main()
