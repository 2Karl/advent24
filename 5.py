PUZZLE_NUMBER: int = 5


def read_input() -> dict[str,list[int] | dict[int,list[int]]]:
    with open(f"input/{PUZZLE_NUMBER}.txt", "r") as file:
        raw:str = file.read()
        pages:list[list[int]] = [[int(x) for x in x.split(",")] for x in raw.splitlines() if "," in x]
        rules:dict = {}
        for rule in [[int(x) for x in x.split("|")] for x in raw.splitlines() if "|" in x]:
            rules.setdefault(rule[0], list()).append(rule[1])
        return {"pages": pages, "rules": rules}


def is_valid(data: list[int], rules: dict[int,list[int]]) -> bool:
    return all(all(x not in data[:i] for x in rules[datum]) for i, datum in enumerate(data) if datum in rules.keys())

def sort(data: list[int], rules: dict[int:list[int]])->list[int]:
    sorted_list:list[int] = []
    for datum in data:
        if datum not in rules.keys() or all(x not in sorted_list for x in rules[datum]):
            sorted_list.append(datum)
        else:
            for i, item in enumerate(sorted_list):
                if item in rules[datum]:
                    sorted_list.insert(i, datum)
                    break
    return sorted_list

def main():
    data: dict[str,list[list[int]] | dict[int:list[int]]] = read_input()

    print(sum(page[len(page) // 2] for page in data["pages"] if is_valid(page, data["rules"])))
    print(sum(sort(page, data["rules"])[len(page) // 2] for page in data["pages"] if not is_valid(page, data["rules"])))


if __name__ == "__main__":
    main()
