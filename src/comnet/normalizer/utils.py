import os.path

# from comnet.normalizer.normalizer import normalize_battles
from comnet.shared.models import Battle, Commander, Country
from comnet.shared.dicts.country_dict import NORMALIZE_COUNTRY_NAME

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
def get_norm_countries(battle_list: list[Battle]) -> set[Country]:
    countries = get_countries(battle_list)
    norm_countries = set()
    for country in countries:
        norm_name = NORMALIZE_COUNTRY_NAME.get(country.name, country.name)
        norm_countries.add(Country(norm_name))
    return norm_countries


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


def get_countries_to_commanders(battle_list: list[Battle]) -> dict[Country, set[Commander]]:
    country_to_commanders: dict[Country, set[Commander]] = {}
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.allegiance:
                    if commander.allegiance not in country_to_commanders:
                        country_to_commanders[commander.allegiance] = set()
                    country_to_commanders[commander.allegiance].add(commander)
    return country_to_commanders

def get_coun_com_batt(battle_list: list[Battle]) -> dict[Country, dict[Commander, set[str]]]:
    country_to_commander_to_battles: dict[Country, dict[Commander, set[str]]] = {}
    for battle in battle_list:
        for side in battle.sides:
            for commander in side.commanders:
                if commander.allegiance:
                    if commander.allegiance not in country_to_commander_to_battles:
                        country_to_commander_to_battles[commander.allegiance] = {}
                    if commander not in country_to_commander_to_battles[commander.allegiance]:
                        country_to_commander_to_battles[commander.allegiance][commander] = set()
                    country_to_commander_to_battles[commander.allegiance][commander].add(battle.name)
    return country_to_commander_to_battles