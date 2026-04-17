import logging
import os

import mwparserfromhell as mwp
from consts import FILES_TO_SKIP_FOR_NOW, INFOBOX_NAMES
from dataclasses import dataclass
from log_utils import setup_logging_parse
import test_objects
from utils import get_all_wiki_files
from enum import Enum

setup_logging_parse()

@dataclass
class InvalidParse:
    def __str__(self) -> str:
        return "Invalid parse"

@dataclass
class Country:
    name: str

    def __str__(self) -> str:
        return self.name

@dataclass 
class Commander:
    name: str
    allegiance: Country | None

    def __str__(self) -> str:
        if self.allegiance:
            return f"{self.name} ({self.allegiance.name})"
        return self.name

@dataclass
class Battle:
    name: str | InvalidParse
    side1Countries: list[Country] | InvalidParse
    side2Countries: list[Country] | InvalidParse

    side1Commanders: list[Commander] | InvalidParse
    side2Commanders: list[Commander] | InvalidParse

    def _list_to_str(self, lst: list[Country] | list[Commander] | InvalidParse, indent: int = 4) -> str:
        if isinstance(lst, InvalidParse):
            return " " * indent + "Invalid parse"
        elif not lst:
            return " " * indent + "None"
        else:
            res = ""
            for item in lst:
                res += " " * indent + str(item) + "\n"
            return res[:-1]

    def __str__(self) -> str:
        res = f"{self.name}:\n"
        res += f"{self._list_to_str(self.side1Countries)}\n"
        res += f"{self._list_to_str(self.side1Commanders, 8)}\n"
        res += f"{self._list_to_str(self.side2Countries)}\n"
        res += f"{self._list_to_str(self.side2Commanders, 8)}\n"
        return res

class CommanderListType(Enum):
    PLAINLIST = 1
    UBL = 2
    BR = 3
    SINGLE = 4
    EMPTY = 5
    PLAINLIST_UPPER = 6
    UNBULLETED_LIST = 7
    NO_LIST_MULTI = 8

def parse_file(file_path: str):
    logging.info(f"Parsing file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    wikicode = mwp.parse(content)

    infobox = get_battle_infobox(wikicode)
    if not infobox:
        # TODO
        return None

    battle_info = get_battle_info(infobox)
    return battle_info

def get_battle_infobox(wikicode: mwp.wikicode.Wikicode) -> mwp.nodes.template.Template | None:
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.strip().lower() in INFOBOX_NAMES:
            return template
    return None

def get_battle_info(infobox: mwp.nodes.template.Template) -> Battle:
    # TODO
    conflict_name = "UNKNOWN"
    wiki_conflict = infobox.get("conflict", default=None)
    if wiki_conflict:
        conflict_name = wiki_conflict.value.strip_code().strip()
    else:
        logging.warning("No conflict name found in infobox")
    name = conflict_name
    side1 = infobox.get("combatant1").value
    side2 = infobox.get("combatant2").value
    countries1 = wiki_to_countries(side1)
    countries2 = wiki_to_countries(side2)
    commander1 = infobox.get("commander1", default=None)
    commander2 = infobox.get("commander2", default=None)
    if not commander1 or not commander2:
        logging.warning("No commander1 or commander2 found in infobox: %s", infobox)
        return Battle(name, countries1, countries2, InvalidParse(), InvalidParse())
    commanders1 = wiki_to_commanders(commander1.value)
    commanders2 = wiki_to_commanders(commander2.value)
    return Battle(name, countries1, countries2, commanders1, commanders2)

def wiki_to_battle_name(name: mwp.wikicode.Wikicode) -> str:
    return name.strip_code().strip()
    

def wiki_to_countries(combatant_code: mwp.wikicode.Wikicode) -> list[Country]:
    countries = []
    for node in combatant_code.nodes:
        # With flagicons
        if isinstance(node, mwp.nodes.Template):
            if node.name.strip().lower() == "flagcountry":
                country_name = node.get(1).value.strip_code().strip()
                countries.append(Country(name=country_name))
        # Without flagicons
        elif isinstance(node, mwp.nodes.Wikilink):
            country_name = node.title.strip_code().strip()
            countries.append(Country(name=country_name))
    return countries


def wiki_to_commanders(commander_code: mwp.wikicode.Wikicode) -> list[Commander] | InvalidParse:
    match get_commander_list_type(commander_code):
        case CommanderListType.PLAINLIST:
            logging.info("Detected plainlist commander format")
            return plainlist_to_list(commander_code)
        case CommanderListType.PLAINLIST_UPPER:
            logging.info("Detected Plainlist commander format")
            return plainlist_upper_to_list(commander_code)
        case CommanderListType.UBL:
            logging.info("Detected ubl commander format")
            return ubl_to_list(commander_code)
        case CommanderListType.UNBULLETED_LIST:
            logging.info("Detected unbulleted list commander format")
            return unbulleted_to_list(commander_code)
        case CommanderListType.BR:
            logging.info("Detected br commander format")
            return br_to_list(commander_code)
        case CommanderListType.SINGLE:
            logging.info("Detected single commander format")
            return [get_commander(commander_code)]
        case CommanderListType.NO_LIST_MULTI:
            logging.info("Detected no-list multi-line commander format")
            return no_list_multi_to_list(commander_code)
        case CommanderListType.EMPTY:
            logging.warning("Detected empty commander format")
            return []
        case None:
            logging.error("Could not determine commander list type for code: %s", commander_code)
            return InvalidParse()

    return InvalidParse()

def get_commander_list_type(commander_code: mwp.wikicode.Wikicode) -> CommanderListType | None:
    for node in commander_code.nodes:
        templates = mwp.parse(str(node)).filter_templates()
        if not templates:
            if "<br />" in str(node):
                return CommanderListType.BR
            continue

        if templates[0].name.strip() == "plainlist":
            return CommanderListType.PLAINLIST
        elif templates[0].name.strip() == "Plainlist":
            return CommanderListType.PLAINLIST_UPPER
        elif templates[0].name.strip().lower() == "ubl":
            return CommanderListType.UBL
        elif templates[0].name.strip().lower() == "unbulleted list":
            return CommanderListType.UNBULLETED_LIST
        elif "<br />"  in str(node).lower():
            return CommanderListType.BR
    
    stripped_code = str(commander_code).strip()

    if len(stripped_code) == 0 or stripped_code == "|":
        return CommanderListType.EMPTY
    
    if stripped_code.count("\n") == 0:
        return CommanderListType.SINGLE
    else:
        return CommanderListType.NO_LIST_MULTI

def plainlist_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    lst = []


    plainlists = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "plainlist")
    if not plainlists or len(plainlists) != 1:
        logging.warning("Expected exactly one plainlist template, got %d. Wikicode: %s", len(plainlists), commander_code)
        return lst
    
    content = plainlists[0].params[0].value.strip()

    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("*"):
            continue

        lst.append(get_commander(mwp.parse(line)))

    return lst

def plainlist_upper_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    commander_code = str(commander_code)
    commander_code = commander_code.replace("{{Plainlist}}", "{{plainlist|")
    commander_code = commander_code.replace("{{Endplainlist}}", "}}")
    return plainlist_to_list(mwp.parse(commander_code))

def ubl_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    lst = []

    ubls = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "ubl")
    if not ubls:
        logging.warning("No ubl templates found. Wikicode: %s", commander_code)
        return lst
    
    # TODO we lose flagicons here
    if len(ubls) == 1:
        country_name = None
        countries = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "flagicon")
        if countries:
            country_name = countries[0].get(1).value.strip_code().strip()
            if len(countries) > 1:
                logging.warning("Expected at most one flagicon template, got %d. Wikicode: %s", len(countries), commander_code)
                return []
            
        for param in ubls[0].params:
            commander = get_commander(mwp.parse(param.value.strip()))
            if country_name:
                commander.allegiance = Country(name=country_name)

            lst.append(commander)

        
        return lst
    
    current_country = None
    for node in commander_code.nodes:
        if isinstance(node, mwp.nodes.Template) and node.name.strip().lower() == "flagicon":
            country_name = node.get(1).value.strip_code().strip()
            current_country = Country(name=country_name)
        elif isinstance(node, mwp.nodes.Template) and node.name.strip().lower() == "ubl":
            if current_country is None:
                logging.warning("Found ubl template without preceding flagicon. Wikicode: %s", commander_code)
            for param in node.params:
                commander = get_commander(mwp.parse(param.value.strip()))
                commander.allegiance = current_country
                lst.append(commander)
    return lst

def unbulleted_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    return ubl_to_list(mwp.parse(str(commander_code).replace("unbulleted list", "ubl")))

def br_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    lst = []

    brs = commander_code.split("<br />")
    for br in brs:
        lst.append(get_commander(mwp.parse(br.strip())))
    return lst

def no_list_multi_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    lst = []
    lines = str(commander_code).split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        lst.append(get_commander(mwp.parse(line)))
    return lst

def get_commander(commander_code: mwp.wikicode.Wikicode) -> Commander:
    # Skip nowrap template
    if commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap"):
        commander_code = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap")[0].get(1).value

    commander = Commander(None, None)
    for temp in commander_code.filter_templates():
        if temp.name.strip().lower() in ["flagicon", "flagdeco"]:
            country_name = temp.get(1).value.strip_code().strip()
            commander.allegiance = Country(name=country_name)
            commander_code.remove(temp)
    
    clean_name = commander_code.strip_code().strip()
    if clean_name and len(clean_name) > 1:
        commander.name = clean_name
    return commander

def print_list_alt(lst: list | InvalidParse):
    if isinstance(lst, InvalidParse):
        print("Invalid parse")
        return
    for item in lst:
        print(item)

if __name__ == "__main__":
    # print_list_alt(wiki_to_commanders(test_objects.com_br))
    # print_list_alt(wiki_to_commanders(test_objects.com_plainlist))
    # print_list_alt(wiki_to_commanders(test_objects.com_ubl))

    # print_list_alt(wiki_to_commanders(test_objects.com_flagdeco2))
    # print_list_alt(wiki_to_commanders(test_objects.com_multiple_plainlist))

    # print(wiki_to_commanders(test_objects.com_almost_empty))
    # print_list_alt(wiki_to_commanders(test_objects.com_almost_empty))
    
    # print_list_alt(wiki_to_commanders(test_objects.com_no_list_multi))

    # exit(0)

    for file_path in get_all_wiki_files():
        file_path = os.path.normpath(file_path)
        filename = file_path.split(os.sep)[-1]
        if filename in FILES_TO_SKIP_FOR_NOW:
            logging.warning("Skipping file: %s", file_path)
            continue
        parse_file(file_path)
        # print(parse_file(file_path))
    