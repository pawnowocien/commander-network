from comnet.normalizer.consts.country_dict import NORMALIZE_COUNTRY_NAME, NAME_TO_COUNTRY
from comnet.normalizer.consts.name_dict import CLEAN_NAME_DICT, COMPLEX_NAME_DICT, LETTER_DICT, SIMPLE_NAME_DICT
from comnet.parser.models import InvalidParse, ParseBattle, ParseCommander, ParseCountry
from comnet.shared.models import Battle, Commander, Country


def normalize_battles(parsed_battles: list[ParseBattle]) -> list[Battle]:
    battles = []
    for parsed_battle in parsed_battles:
        battle = Battle(
            raw_name=parsed_battle.raw_name,
            name=_normalize_battle_name(parsed_battle.name),
            side1Countries=_normalize_countries(parsed_battle.side1Countries),
            side2Countries=_normalize_countries(parsed_battle.side2Countries),
            side1Commanders=_normalize_commanders(parsed_battle.side1Commanders),
            side2Commanders=_normalize_commanders(parsed_battle.side2Commanders),
        )
        battles.append(battle)
    return battles
        

def _normalize_countries(parsed_countries: list[ParseCountry] | InvalidParse) -> list[Country]:
    if isinstance(parsed_countries, InvalidParse):
        return []
    return [_normalize_country(parsed_country) for parsed_country in parsed_countries]
    
def _normalize_country(parsed_country: ParseCountry) -> Country:
    country_name = parsed_country.name

    if country_name in NORMALIZE_COUNTRY_NAME.keys():
        country_name = NORMALIZE_COUNTRY_NAME[country_name]
    
    return Country(country_name)

def _normalize_commanders(parsed_commanders:list[ParseCommander] | InvalidParse) -> list[Commander]:
    if isinstance(parsed_commanders, InvalidParse):
        return []
    
    return [_normalize_commander(commander) for commander in parsed_commanders]


def _normalize_commander(commander: ParseCommander) -> Commander:
    normalized_name = _normalize_commander_name(commander.name)
    normalized_allegiance = _normalize_allegiance(commander.allegiance, normalized_name)

    country = Country(normalized_allegiance)
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


def _normalize_allegiance(allegiance: ParseCountry | None, norm_name: str) -> str:
    if allegiance:
        country = allegiance.name

        if not country in NORMALIZE_COUNTRY_NAME:
            
            # TODO log
            return "(!) " + country
        return NORMALIZE_COUNTRY_NAME[country]

    if norm_name in NAME_TO_COUNTRY:
        return NAME_TO_COUNTRY[norm_name]

    # print("No allegiance for commander: %s" % commander.name)
    return "None"


def _normalize_battle_name(name: str | InvalidParse) -> str:
    if isinstance(name, InvalidParse):
        return "ERROR" # TODO log
    
    return name.strip()