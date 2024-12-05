import re, math

PUZZLE_NUMBER: int = 3


def read_input() -> list[list[int] | str]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        return [[int(x) for x in row.split(",")] if "d" not in row else row for row in
                re.findall('(do(?:n\'t)?(?=\\(\\))|(?<=mul\\()\\d{1,3},\\d{1,3}(?=\\)))', file.read())]


def main():
    total: int = 0
    data = read_input()
    enabled: bool = True
    for datum in data:
        if datum == "do":
            enabled = True
        elif datum == "don't":
            enabled = False
        elif enabled:
            total += math.prod(datum)

    print(total)


if __name__ == "__main__":
    main()
