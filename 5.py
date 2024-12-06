PUZZLE_NUMBER: int = 5


def read_input():
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        raw = file.read()
        pages = [[int(x) for x in x.split(",")] for x in raw.splitlines() if "," in x]
        rules = {}
        for rule in [[int(x) for x in x.split("|")] for x in raw.splitlines() if "|" in x]:
            rules.setdefault(rule[0], list()).append(rule[1])
        return {"pages": pages, "rules": rules}


def is_valid(data: list[int], rules: dict[int:list[int]]) -> bool:
    return all(all(x not in data[:i] for x in rules[datum]) for i, datum in enumerate(data) if datum in rules.keys())


def main():
    data = read_input()
    print(sum(page[len(page) // 2] for page in data["pages"] if is_valid(page, data["rules"])))


if __name__ == "__main__":
    main()
