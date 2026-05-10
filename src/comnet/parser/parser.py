import logging
import os

import mwparserfromhell as mwp
from comnet.shared.consts import BR_NAMES, FILES_TO_SKIP, INFOBOX_NAMES
from comnet.shared.log_utils import setup_logging_parse
from comnet.parser.combatant_parser import parse_combatant
from comnet.parser.commander_parser import parse_commander
from comnet.shared.utils import get_all_wiki_files
from .models import ParseBattle, InvalidParse

setup_logging_parse()

def parse_files(file_paths: list[str] | str | None = None) -> list[ParseBattle]:
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    elif file_paths is None:
        file_paths = get_all_wiki_files()
    battles = []
    for file_path in file_paths:
        battle = _parse_single_file(file_path)
        if battle:
            battles.append(battle)
    return battles

def _parse_single_file(file_path: str) -> ParseBattle | None:
    logging.info(f"Parsing file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    wikicode = mwp.parse(content)

    infobox = _get_battle_infobox(wikicode)
    if not infobox:
        logging.warning("No battle infobox found in file: %s", file_path)
        return None

    raw_battle_name = file_path.split(os.sep)[-1].replace(".txt", "").replace("__", "/")
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
    # conflict_name = get_conflict_name(infobox)
    # if conflict_name == "":
    #     if alt_title:
    #         logging.warning("No conflict name found. Using alt title: %s", alt_title)
    #         conflict_name = alt_title
    #     else:
    #         logging.error("No conflict name found, even alt title is not available. Skipping battle.")
    #         return None
        

    side1 = infobox.get("combatant1", default=None)
    side2 = infobox.get("combatant2", default=None)
    if not side1 or not side2:
        logging.warning("No combatant1 or combatant2 found in infobox: %s", infobox)
        return ParseBattle(raw_battle_name, conflict_name, InvalidParse(), InvalidParse(), InvalidParse(), InvalidParse())
    countries1 = parse_combatant(side1.value)
    countries2 = parse_combatant(side2.value)

    commander1 = infobox.get("commander1", default=None)
    commander2 = infobox.get("commander2", default=None)
    if not commander1 or not commander2:
        logging.warning("No commander1 or commander2 found in infobox: %s", infobox)
        return ParseBattle(raw_battle_name, conflict_name, countries1, countries2, InvalidParse(), InvalidParse())
    commanders1 = parse_commander(commander1.value)
    commanders2 = parse_commander(commander2.value)

    return ParseBattle(raw_battle_name, conflict_name, countries1, countries2, commanders1, commanders2)

# def _get_conflict_name(infobox: mwp.nodes.template.Template) -> str:
#     wiki_conflict = infobox.get("conflict", default=None)
#     if wiki_conflict:
#         conflict_name = str(wiki_conflict.value)
#         for br in BR_NAMES:
#             if br in conflict_name:
#                 name = conflict_name.split(br)[0].strip()
#                 logging.warning("Conflict name contains line break, choosing the first title: %s", name)
#                 return name
            
#         return wiki_conflict.value.strip_code().strip()
#     return ""

# def _wiki_to_battle_name(name: mwp.wikicode.Wikicode) -> str:
#     return name.strip_code().strip()
    

# def parse_all_files() -> list[ParseBattle]:
#     battles = []
#     t1 = []
#     t2 = []
#     for file_path in get_all_wiki_files():
#         file_path = os.path.normpath(file_path)
#         filename = file_path.split(os.sep)[-1]
#         if "offensive" in filename.lower():
#             t1.append('"' + filename + '",')
#             t2.append("https://en.wikipedia.org/wiki/" + filename.replace(".txt", "").replace("__", "/"))
#         if filename in FILES_TO_SKIP:
#             logging.info("Skipping file: %s", file_path)
#             continue
#         battle = _parse_single_file(file_path)
#         if battle and battle.name:
#             battles.append(battle)
#         else:
#             logging.error("Battle doesn't have a name, skipping: %s", file_path)

#     for a in t1:
#         print(a)
#     for a in t2:
#         print(a)
#     return battles


if __name__ == "__main__":    
    # battles = parse_all_files()

    pass
    # test_com_pattern(test_objects.com_flagicon_image)
    # parse_commander(test_objects.com_single_ill)
    # TODO Petsamo_expeditions.txt has two infoboxes