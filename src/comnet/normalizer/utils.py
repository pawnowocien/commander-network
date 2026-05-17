import os.path

# from comnet.normalizer.normalizer import normalize_battles
from comnet.shared.models import Battle, Commander, Country
from comnet.normalizer.consts.country_dict import NORMALIZE_COUNTRY_NAME
from comnet.shared.utils import rawname_to_link

# def get_all_battles() -> list[Battle]:
#     from comnet.parser.parser import parse_files
#     return normalize_battles(parse_files())

def get_commanders(battle_list: list[Battle]) -> set[Commander]:
    commanders = set()
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.name:
                    commanders.add(commander)
    return commanders
def get_countries(battle_list: list[Battle]) -> set[Country]:
    countries = set()
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.allegiance:
                    countries.add(commander.allegiance)
    return countries



def save_battles(battle_list: list[Battle], file_path: str = "tmp/battles.txt") -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for battle in sorted(battle_list, key=lambda b: b.name):
            f.write(f"{battle.name}\n")
def save_commanders(battle_list: list[Battle], file_path: str = "tmp/commanders.txt") -> None:
    commanders = get_commanders(battle_list)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for commander in sorted(commanders, key=lambda c: c.name):
            f.write(f"{commander.name}\n")
def save_countries(battle_list: list[Battle], file_path: str = "tmp/countries.txt") -> None:
    countries = get_countries(battle_list)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for country in sorted(countries, key=lambda c: str(c)):
            f.write(f"{country}\n")



def get_all_commander_names(battle_list: list[Battle]) -> dict[str, set[str]]:
    names = {}
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
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

def get_commanders_country(commander: Commander) -> str | None:
    if commander.allegiance:
        allegiance_str = str(commander.allegiance)
        if allegiance_str in NORMALIZE_COUNTRY_NAME.keys():
            return NORMALIZE_COUNTRY_NAME[allegiance_str]
        return allegiance_str
    return None

def save_commanders_and_countries(battle_list: list[Battle], file_path: str = "tmp/commanders_and_countries.txt") -> None:
    dict_commanders: dict[str, set[str]] = {}
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.name not in dict_commanders:
                    dict_commanders[commander.name] = set()
                country = get_commanders_country(commander)
                if country:
                    dict_commanders[commander.name].add(country)
    with open(file_path, "w", encoding="utf-8") as f:
        for commander_name in sorted(dict_commanders):
            countries = ", ".join(sorted(dict_commanders[commander_name]))
            if not countries:
                countries = "Unknown"
            f.write(f"{commander_name}\n{countries}\n-----\n")

def save_commander_countries(commanders: set[Commander], file_path: str = "tmp/commander_countries.txt") -> None:
    countries = set()
    for commander in commanders:
        if commander.allegiance:
            allegiance_str = str(commander.allegiance)
            if allegiance_str in NORMALIZE_COUNTRY_NAME.keys():
                allegiance_str = NORMALIZE_COUNTRY_NAME[allegiance_str]
            # elif allegiance_str not in countries:
            #     print(allegiance_str)
            countries.add(allegiance_str)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for country in sorted(countries):
            f.write(f"\"{country}\": \"\",\n")

def save_commanders_without_allegiance(battle_list: list[Battle]) -> None:
    commanders = dict()
    commanders_with_allegiance = set()
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.name not in commanders:
                    commanders[commander.name] = set()
                commanders[commander.name].add(rawname_to_link(battle.raw_name))

                if not commander.allegiance:
                    continue

                country_name = commander.allegiance.name
                if country_name == "None" or country_name == "":
                    continue
                commanders_with_allegiance.add(commander.name)
    
    for commander in commanders_with_allegiance:
        commanders.pop(commander, None)
    
    with open("tmp/commanders_without_allegiance.txt", "w", encoding="utf-8") as f:
        f.write("TOTAL: " + str(len(commanders)) + "\n\n")

        for commander_name in sorted(commanders):
            battles = "\n".join(sorted(commanders[commander_name]))
            f.write(f"{commander_name}:\nbattles: \n{battles}\n-----\n")


def print_commanders_with_allegiance(battle_list: list[Battle]) -> None:
    dict_commanders = {}
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.name not in dict_commanders:
                    dict_commanders[commander.name] = (set(), set())
                country = get_commanders_country(commander)
                
                if country:
                    dict_commanders[commander.name][0].add(country)
                
                dict_commanders[commander.name][1].add(rawname_to_link(battle.raw_name))
                    
    
    for commander_name in sorted(dict_commanders):
        countries = ", ".join(sorted(dict_commanders[commander_name][0]))
        if not countries:
            countries = "Unknown"
        
        battles = "\n".join(sorted(dict_commanders[commander_name][1]))
        print(f"{commander_name}:\n{countries}\nbattles: \n{battles}\n-----")

def get_all_countries_list(battle_list: list[Battle]) -> list[Country]:
    countries: set[Country] = set()
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                country = commander.allegiance
                if country:
                    countries.add(country)
    return sorted(countries, key=lambda c: str(c))