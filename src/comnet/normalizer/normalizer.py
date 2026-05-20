import itertools
import json
import os
from dataclasses import asdict

from comnet.normalizer.consts.country_dict import NORMALIZE_COUNTRY_NAME, NAME_TO_COUNTRY
from comnet.normalizer.consts.name_dict import CLEAN_NAME_DICT, COMPLEX_NAME_DICT, LETTER_DICT, SIMPLE_NAME_DICT
from comnet.shared.models import BattleRow, CommanderRow
from comnet.normalizer.utils import get_commanders, get_norm_countries
from comnet.parser.models import ParseBattle, ParseCommander, ParseCountry
from comnet.shared.models import Battle, Commander, Country, Side
from comnet.shared.utils import rawname_to_safename


def normalize_battles(parsed_battles: list[ParseBattle]) -> list[Battle]:
    battles = []
    for i, parsed_battle in enumerate(parsed_battles):
        print(f"\rNormalizing battles... {i+1}/{len(parsed_battles)}", end="")
        sides = []
        for parsed_side in parsed_battle.sides:
            countries = _normalize_countries(parsed_side.countries)
            commanders = _normalize_commanders(parsed_side.commanders)
            sides.append(Side(countries, commanders))
            
        battle = Battle(
            raw_name=parsed_battle.raw_name,
            name=_normalize_battle_name(parsed_battle.name),
            sides=sides
        )
        battles.append(battle)
    print()
    return battles
        

def _normalize_countries(parsed_countries: list[ParseCountry]) -> list[Country]:
    return [_normalize_country(parsed_country) for parsed_country in parsed_countries]
    
def _normalize_country(parsed_country: ParseCountry) -> Country:
    country_name = parsed_country.name

    if country_name in NORMALIZE_COUNTRY_NAME.keys():
        country_name = NORMALIZE_COUNTRY_NAME[country_name]
    
    return Country(country_name)

def _normalize_commanders(parsed_commanders:list[ParseCommander]) -> list[Commander]:    
    return [_normalize_commander(commander) for commander in parsed_commanders]


def _normalize_commander(commander: ParseCommander) -> Commander:
    normalized_name = _normalize_commander_name(commander.name)
    normalized_allegiance = _normalize_allegiance(commander.allegiance, normalized_name)

    country = Country(", ".join(normalized_allegiance)) # TODO hack for now
    return Commander(normalized_name, country)


def _normalize_commander_name(name: str) -> str:
    # Go through dicts

    for k, v in LETTER_DICT.items():
        name = name.replace(k, v)
    
    parts = name.split(" ")
    first_name = parts[0]
    if first_name in SIMPLE_NAME_DICT:
        parts[0] = SIMPLE_NAME_DICT[first_name]
        name = " ".join(parts)

    for first_name in SIMPLE_NAME_DICT.keys():
        split_name = name.split(" ")
        if split_name[0] == first_name:
            name = SIMPLE_NAME_DICT[first_name]
            for i in range(1, len(split_name)):
                name += " " + split_name[i]
            break

    if name in CLEAN_NAME_DICT:
        name = CLEAN_NAME_DICT[name]
    
    if name in COMPLEX_NAME_DICT:
        name = COMPLEX_NAME_DICT[name]

    return name.strip()


def _normalize_allegiance(allegiance: list[ParseCountry], norm_name: str) -> set[str]:
    countries = set()

    for country in allegiance:
        country_name = country.name

        if not country_name in NORMALIZE_COUNTRY_NAME:
            
            # TODO log
            countries.add("(!) " + country_name)
            continue
        countries.add(NORMALIZE_COUNTRY_NAME[country_name])

    if len(countries) > 0:
        return countries

    if norm_name in NAME_TO_COUNTRY:
        return {NAME_TO_COUNTRY[norm_name]}

    return set()


def _normalize_battle_name(name: str) -> str:
    return name.strip()

def save_normalized(battles: list[Battle], output_file: str = "data/normalized/normalized_battles.json") -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    battle_dict = [asdict(battle) for battle in battles]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(battle_dict, f, ensure_ascii=False, indent=4)

def save_to_csv(battles: list[Battle], output_dir: str = "data/normalized/") -> None:
    os.makedirs(output_dir, exist_ok=True)

    commanders = get_commanders(battles)
    commander_rows = _get_commander_rows(commanders)

    battle_rows = _get_battle_rows(battles)

    os.makedirs(os.path.dirname(output_dir), exist_ok=True)
    with open(os.path.join(output_dir, "battles.csv"), "w", encoding="utf-8") as f:
        for row in battle_rows:
            f.write(f"{rawname_to_safename(row.name)};{row.commander1};{row.commander2}\n")
    
    with open(os.path.join(output_dir, "commanders.csv"), "w", encoding="utf-8") as f:
        for row in commander_rows:
            f.write(f"{row.name};{row.country}\n")

def _get_commander_rows(commanders: set[Commander]) -> list[CommanderRow]:
    comm_to_country: dict[str, set[str]] = {}
    for commander in commanders:
        if commander.name not in comm_to_country:
            comm_to_country[commander.name] = set()
        if commander.allegiance.name:
            comm_to_country[commander.name].add(commander.allegiance.name)
    
    commander_rows = []
    for commander_name, countries in comm_to_country.items():
        if commander_name in NAME_TO_COUNTRY:
            commander_rows.append(CommanderRow(commander_name, NAME_TO_COUNTRY[commander_name]))
            continue
        if len(countries) == 1:
            commander_rows.append(CommanderRow(commander_name, list(countries)[0]))
            continue

        print(f"Warning: Commander {commander_name} has {len(countries)} countries: {countries}")
    return commander_rows


def _get_battle_rows(battles: list[Battle]) -> list[BattleRow]:
    rows = []
    for battle in battles:
        for side in battle.sides:
            for commander1, commander2 in itertools.combinations(side.commanders, 2):
                rows.append(BattleRow(battle.name, commander1.name, commander2.name))
    return rows

def main():
    with open("data/parsed/parsed_battles.json", "r", encoding="utf-8") as f:
        parsed_battle_dicts = json.load(f)
        parsed_battles = [ParseBattle.from_dict(battle_dict) for battle_dict in parsed_battle_dicts]
        battles = normalize_battles(parsed_battles)
        save_to_csv(battles)

if __name__ == "__main__":
    main()