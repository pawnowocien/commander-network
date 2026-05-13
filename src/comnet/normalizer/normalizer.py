import json
import os
from dataclasses import asdict

from comnet.normalizer.consts.country_dict import NORMALIZE_COUNTRY_NAME, NAME_TO_COUNTRY
from comnet.normalizer.consts.name_dict import CLEAN_NAME_DICT, COMPLEX_NAME_DICT, LETTER_DICT, SIMPLE_NAME_DICT
from comnet.parser.models import ParseBattle, ParseCommander, ParseCountry
from comnet.shared.models import Battle, Commander, Country, Side


def normalize_battles(parsed_battles: list[ParseBattle]) -> list[Battle]:
    battles = []
    for parsed_battle in parsed_battles:
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

    # print("No allegiance for commander: %s" % commander.name)
    return set()


def _normalize_battle_name(name: str) -> str:
    return name.strip()

def save_normalized(battles: list[Battle], output_file: str = "data/normalized/normalized_battles.json") -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    battle_dict = [asdict(battle) for battle in battles]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(battle_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    with open("data/parsed/parsed_battles.json", "r", encoding="utf-8") as f:
        parsed_battle_dicts = json.load(f)
    
    