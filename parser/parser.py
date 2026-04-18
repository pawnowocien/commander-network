import logging
import os

import mwparserfromhell as mwp
from consts import FILES_TO_SKIP, INFOBOX_NAMES
from log_utils import setup_logging_parse
from parser.combatant_parser import parse_combatant
from parser.commander_parser import parse_commander
from utils import get_all_wiki_files
from parser.models import Battle, InvalidParse

setup_logging_parse()

def parse_file(file_path: str) -> Battle | None:
    logging.info(f"Parsing file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    wikicode = mwp.parse(content)

    infobox = get_battle_infobox(wikicode)
    if not infobox:
        logging.warning("No battle infobox found in file: %s", file_path)
        return None

    return get_battle_info(infobox)

def get_battle_infobox(wikicode: mwp.wikicode.Wikicode) -> mwp.nodes.template.Template | None:
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.strip().lower() in INFOBOX_NAMES:
            return template
    return None

def get_battle_info(infobox: mwp.nodes.template.Template) -> Battle | None:
    # TODO
    conflict_name = "UNKNOWN"
    wiki_conflict = infobox.get("conflict", default=None)
    if wiki_conflict:
        conflict_name = wiki_conflict.value.strip_code().strip()
    else:
        logging.warning("No conflict name found in infobox")
    name = conflict_name

    side1 = infobox.get("combatant1", default=None)
    side2 = infobox.get("combatant2", default=None)
    if not side1 or not side2:
        logging.warning("No combatant1 or combatant2 found in infobox: %s", infobox)
        return Battle(name, InvalidParse(), InvalidParse(), InvalidParse(), InvalidParse())
    countries1 = parse_combatant(side1.value)
    countries2 = parse_combatant(side2.value)

    commander1 = infobox.get("commander1", default=None)
    commander2 = infobox.get("commander2", default=None)
    if not commander1 or not commander2:
        logging.warning("No commander1 or commander2 found in infobox: %s", infobox)
        return Battle(name, countries1, countries2, InvalidParse(), InvalidParse())
    commanders1 = parse_commander(commander1.value)
    commanders2 = parse_commander(commander2.value)

    return Battle(name, countries1, countries2, commanders1, commanders2)

def wiki_to_battle_name(name: mwp.wikicode.Wikicode) -> str:
    return name.strip_code().strip()
    
def print_list_alt(lst: list | InvalidParse):
    if isinstance(lst, InvalidParse):
        print("Invalid parse")
        return
    for item in lst:
        print(item)

def parse_all():
    for file_path in get_all_wiki_files():
        file_path = os.path.normpath(file_path)
        filename = file_path.split(os.sep)[-1]
        if filename in FILES_TO_SKIP:
            logging.info("Skipping file: %s", file_path)
            continue
        parse_file(file_path)

def test_com_pattern(wikicode: mwp.wikicode.Wikicode):
    print_list_alt(parse_commander(wikicode))
    print("----")


if __name__ == "__main__":    
    parse_all()
