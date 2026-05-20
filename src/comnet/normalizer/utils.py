import os.path

# from comnet.normalizer.normalizer import normalize_battles
from comnet.shared.models import Battle, Commander, Country
from comnet.normalizer.consts.country_dict import NORMALIZE_COUNTRY_NAME
from comnet.shared.utils import rawname_to_link

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