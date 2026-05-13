import json
import logging
from dataclasses import asdict
import os

import mwparserfromhell as mwp
from comnet.parser.consts import HANDLED_EXCEPTION_BATTLES, INFOBOX_NAMES
from comnet.parser.test import test_objects
from comnet.shared.consts import BATTLES_EXCEPTIONS
from comnet.shared.log_utils import setup_logging_parse
from comnet.parser.combatant_parser import parse_combatant
from comnet.parser.commander_parser import parse_commander
from comnet.shared.utils import filepath_to_rawname, get_filtered_wiki_files
from comnet.parser.models import ParseBattle, ParseSide

setup_logging_parse()

def parse_files(file_paths: list[str] | str | None = None) -> list[ParseBattle]:
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    elif file_paths is None:
        file_paths = get_filtered_wiki_files()
    battles = []
    for file_path in file_paths:
        battle = _parse_single_file(file_path)
        if battle:
            battles.append(battle)
    return battles

def _parse_single_file(file_path: str) -> ParseBattle | None:
    raw_battle_name = filepath_to_rawname(file_path)
    
    logging.info(f"Parsing file: {file_path}")

    if raw_battle_name in BATTLES_EXCEPTIONS:
        if raw_battle_name in HANDLED_EXCEPTION_BATTLES:
            logging.info(f"Using hardcoded battle info for {raw_battle_name}")
            return HANDLED_EXCEPTION_BATTLES[raw_battle_name]
        else:
            logging.error(f"Battle {raw_battle_name} is in EXCEPTIONS but not in HANDLED_EXCEPTION_BATTLES")
            return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    wikicode = mwp.parse(content)

    infobox = _get_battle_infobox(wikicode)
    if not infobox:
        logging.warning("No battle infobox found in file: %s", file_path)
        return None

    return _get_battle_info(infobox, raw_battle_name=raw_battle_name)

def _get_battle_infobox(wikicode: mwp.wikicode.Wikicode) -> mwp.nodes.template.Template | None:
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.strip().lower() in INFOBOX_NAMES:
            return template
    return None

def _get_battle_info(infobox: mwp.nodes.template.Template, raw_battle_name: str) -> ParseBattle | None:
    # TODO change after parsing multiple battles per file
    conflict_name = raw_battle_name.replace("_", " ") or ""


    combatant_codes = []
    commander_codes = []
    i = 1
    while True:
        combatant_code = infobox.get(f"combatant{i}", default=None)
        commander_code = infobox.get(f"commander{i}", default=None)

        combatant_present = combatant_code is not None and combatant_code.value.strip() != ""
        commander_present = commander_code is not None and commander_code.value.strip() != ""

        # There cant be more commanders than combatants:
        if commander_present and not combatant_present:
            logging.error("Invalid infobox format: combatant%d and commander%d mismatch", i, i)
            break
        
        if not combatant_present and not commander_present:
            break

        combatant_codes.append(combatant_code)
        if commander_present:
            commander_codes.append(commander_code)
        i += 1

    sides_num = len(combatant_codes)
    if sides_num == 2:
        logging.info("Found %d sides", sides_num)
    else:
        logging.warning("Found %d sides", sides_num)

    sides: list[ParseSide] = []
    for combatant_code, commander_code in zip(combatant_codes, commander_codes):
        countries = parse_combatant(combatant_code.value)
        commanders = []
        if commander_code:
            commanders = parse_commander(commander_code.value)
        sides.append(ParseSide(countries, commanders))

    return ParseBattle(raw_battle_name, conflict_name, sides)

def save_parse(file_paths: list[str] | str | None = None, output_file: str = "data/parsed/parsed_battles.json") -> None:
    battles = parse_files(file_paths)
    save_battles(battles, output_file)

def save_battles(battles: list[ParseBattle], output_file: str = "data/parsed/parsed_battles.json") -> None:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    battle_dict = [asdict(battle) for battle in battles]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(battle_dict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    save_parse()