from models.models import Battle, InvalidParse
import os.path

def get_all_commander_names(battle_list: list[Battle]) -> dict[str, set[str]]:
    names = {}
    for battle in battle_list:
        for commander_list in [battle.side1Commanders, battle.side2Commanders]:
            if not isinstance(commander_list, InvalidParse):
                for commander in commander_list:
                    if not commander.name:
                        print(f"Warning: Commander with empty name in battle {battle.name}")
                    else:
                        if commander.name not in names:
                            names[commander.name] = set()
                        names[commander.name].add(battle.name)

    return names


def save_commander_names(battle_list: list[Battle], file_path: str = "tmp/commander_names.txt") -> None:
    names = get_all_commander_names(battle_list)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for name in sorted(names):
            battles = ", ".join(sorted(names[name]))
            f.write(f"{name}\n{battles}\n-----\n")


if __name__ == "__main__":
    from parser.parser import parse_all_files

    save_commander_names(parse_all_files())