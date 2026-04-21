import logging
import os

import mwparserfromhell as mwp
from consts import BR_NAMES, FILES_TO_SKIP, INFOBOX_NAMES
from log_utils import setup_logging_parse
from parser import test_objects
from parser.combatant_parser import parse_combatant
from parser.commander_parser import parse_commander
from utils import get_all_wiki_files
from models.models import Battle, InvalidParse

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

    alt_battle_name = file_path.split(os.sep)[-1].replace(".txt", "").replace("__", "/").replace("_", " ")
    return get_battle_info(infobox, alt_title=alt_battle_name)

def get_battle_infobox(wikicode: mwp.wikicode.Wikicode) -> mwp.nodes.template.Template | None:
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.strip().lower() in INFOBOX_NAMES:
            return template
    return None

def get_battle_info(infobox: mwp.nodes.template.Template, alt_title: str | None = None) -> Battle | None:
    # TODO

    conflict_name = get_conflict_name(infobox)
    if conflict_name == "":
        if alt_title:
            logging.warning("No conflict name found. Using alt title: %s", alt_title)
            conflict_name = alt_title
        else:
            logging.error("No conflict name found, even alt title is not available. Skipping battle.")
            return None
        

    side1 = infobox.get("combatant1", default=None)
    side2 = infobox.get("combatant2", default=None)
    if not side1 or not side2:
        logging.warning("No combatant1 or combatant2 found in infobox: %s", infobox)
        return Battle(conflict_name, InvalidParse(), InvalidParse(), InvalidParse(), InvalidParse())
    countries1 = parse_combatant(side1.value)
    countries2 = parse_combatant(side2.value)

    commander1 = infobox.get("commander1", default=None)
    commander2 = infobox.get("commander2", default=None)
    if not commander1 or not commander2:
        logging.warning("No commander1 or commander2 found in infobox: %s", infobox)
        return Battle(conflict_name, countries1, countries2, InvalidParse(), InvalidParse())
    commanders1 = parse_commander(commander1.value)
    commanders2 = parse_commander(commander2.value)

    return Battle(conflict_name, countries1, countries2, commanders1, commanders2)

def get_conflict_name(infobox: mwp.nodes.template.Template) -> str:
    wiki_conflict = infobox.get("conflict", default=None)
    if wiki_conflict:
        conflict_name = str(wiki_conflict.value)
        for br in BR_NAMES:
            if br in conflict_name:
                name = conflict_name.split(br)[0].strip()
                logging.warning("Conflict name contains line break, choosing the first title: %s", name)
                return name
            
        return wiki_conflict.value.strip_code().strip()
    return ""

def wiki_to_battle_name(name: mwp.wikicode.Wikicode) -> str:
    return name.strip_code().strip()
    
def print_list_alt(lst: list | InvalidParse):
    if isinstance(lst, InvalidParse):
        print("Invalid parse")
        return
    for item in lst:
        print(item)

def parse_all_files() -> list[Battle]:
    battles = []
    for file_path in get_all_wiki_files():
        file_path = os.path.normpath(file_path)
        filename = file_path.split(os.sep)[-1]
        if filename in FILES_TO_SKIP:
            logging.info("Skipping file: %s", file_path)
            continue
        battle = parse_file(file_path)
        if battle and battle.name:
            battles.append(battle)
        else:
            logging.error("Battle doesn't have a name, skipping: %s", file_path)
    return battles

def test_com_pattern(wikicode: mwp.wikicode.Wikicode):
    print_list_alt(parse_commander(wikicode))
    print("----")


if __name__ == "__main__":    
    parse_all_files()
    # test_com_pattern(test_objects.com_wia)
    # parse_commander(test_objects.com_single_ill)
    # TODO Petsamo_expeditions.txt has two infoboxes