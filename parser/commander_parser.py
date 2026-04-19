import mwparserfromhell as mwp
from consts import BR_NAMES, FLAG_ICON_TEMPLATE_NAMES, MULTI_ALLEGIANCE_COMMANDER_NAMES
from models.models import InvalidParse, Commander, Country, CommanderListType
import logging


def parse_commander(commander_code: mwp.wikicode.Wikicode) -> list[Commander] | InvalidParse:
    commanders = []
    match get_commander_list_type(commander_code):
        case CommanderListType.PLAINLIST:
            logging.info("Detected plainlist commander format")
            commanders = plainlist_to_list(commander_code)
        case CommanderListType.PLAINLIST_UPPER:
            logging.info("Detected Plainlist commander format")
            commanders = plainlist_upper_to_list(commander_code)
        case CommanderListType.TREE_LIST:
            logging.info("Detected tree list commander format")
            commanders = tree_list_to_list(commander_code)
        case CommanderListType.UBL:
            logging.info("Detected ubl commander format")
            commanders = ubl_to_list(commander_code)
        case CommanderListType.UBLI:
            logging.info("Detected ubli commander format")
            commanders = ubli_to_list(commander_code)
        case CommanderListType.UNBULLETED_LIST:
            logging.info("Detected unbulleted list commander format")
            commanders = unbulleted_to_list(commander_code)
        case CommanderListType.BR:
            logging.info("Detected br commander format")
            commanders = br_to_list(commander_code)
        case CommanderListType.SINGLE:
            logging.info("Detected single commander format")
            commanders = [get_commander(commander_code)]
        case CommanderListType.NO_LIST_MULTI:
            logging.info("Detected no-list multi-line commander format")
            commanders = no_list_multi_to_list(commander_code)
        case CommanderListType.EMPTY:
            logging.warning("Detected empty commander format")
            return []
        case None:
            logging.error("Could not determine commander list type for code: %s", commander_code)
            return InvalidParse()
        case _:
            logging.error("Unhandled commander list type for code: %s", commander_code)
            return InvalidParse()
    return clear_list(commanders)

def clear_list(commander_list: list[Commander | None]) -> list[Commander]:
    lst = []
    for commander in commander_list:
        if commander:
            lst.append(commander)
    return lst

def get_commander_list_type(commander_code: mwp.wikicode.Wikicode) -> CommanderListType | None:
    for node in commander_code.nodes:
        templates = mwp.parse(str(node)).filter_templates()
        if not templates:
            if contains_br(node):
                return CommanderListType.BR
            continue

        if templates[0].name.strip() == "plainlist":
            return CommanderListType.PLAINLIST
        elif templates[0].name.strip() == "Plainlist":
            return CommanderListType.PLAINLIST_UPPER
        elif templates[0].name.strip().lower() == "tree list":
            return CommanderListType.TREE_LIST
        elif templates[0].name.strip().lower() == "ubl":
            return CommanderListType.UBL
        elif templates[0].name.strip().lower() == "ubli":
            return CommanderListType.UBLI
        elif templates[0].name.strip().lower() == "unbulleted list":
            return CommanderListType.UNBULLETED_LIST
        elif contains_br(node):
            return CommanderListType.BR
    
    stripped_code = str(commander_code).strip()

    if len(stripped_code) == 0 or stripped_code == "|":
        return CommanderListType.EMPTY
    
    if stripped_code.count("\n") == 0:
        return CommanderListType.SINGLE
    else:
        return CommanderListType.NO_LIST_MULTI

def contains_br(node: mwp.nodes.Node) -> bool:
    for br_name in BR_NAMES:
        if br_name in str(node):
            return True
    return False

def plainlist_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
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

def plainlist_upper_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    commander_code = str(commander_code)
    commander_code = commander_code.replace("{{Plainlist}}", "{{plainlist|")
    commander_code = commander_code.replace("{{Endplainlist}}", "}}")
    return plainlist_to_list(mwp.parse(commander_code))

def tree_list_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    commander_code = str(commander_code)
    commander_code = commander_code.replace("{{tree list}}", "{{plainlist|")
    commander_code = commander_code.replace("{{tree list/end}}", "}}")
    return plainlist_to_list(mwp.parse(commander_code))

def ubl_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    lst = []

    current_code = ""
    for node in commander_code.nodes:
        current_code += str(node)
        if isinstance(node, mwp.nodes.Template) and node.name.strip().lower() == "ubl":
            lst.extend(single_ubl_to_list(mwp.parse(current_code)))
            current_code = ""

    return lst

def single_ubl_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    """
    Can be either:
    - `flagicon? list[commander]`
    - `list[flagicon? commander]`
    """
    ubl_templates = get_ubl_templates(commander_code)
    if not ubl_templates or len(ubl_templates) != 1:
        logging.error("Expected exactly one ubl template for single ubl commander format, got %d. Wikicode: %s", len(ubl_templates), commander_code)
        return []
    
    lst = []

    # flagicon? list[commander]
    if is_template_flagicon(commander_code.filter_templates()[0]):
        country = commander_code.filter_templates()[0].get(1).value.strip_code().strip() if commander_code.filter_templates() else None
        for param in ubl_templates[0].params:
            commander = get_commander(mwp.parse(param.value.strip()))
            if country and commander.allegiance:
                logging.error("Detected commander with multiple allegiances in single ubl commander format. Wikicode: %s", commander_code)
            elif country:
                commander.allegiance = Country(name=country)
            lst.append(commander)

    # list[flagicon? commander]
    else:
        for param in ubl_templates[0].params:
            lst.append(get_commander(mwp.parse(param.value.strip())))
    return lst

def get_flagicon_templates(wikicode: mwp.wikicode.Wikicode) -> list[mwp.nodes.template.Template]:
    return wikicode.filter_templates(matches=lambda t: t.name.strip().lower() in FLAG_ICON_TEMPLATE_NAMES)
def get_ubl_templates(wikicode: mwp.wikicode.Wikicode) -> list[mwp.nodes.template.Template]:
    return wikicode.filter_templates(matches=lambda t: t.name.strip().lower() == "ubl")

def is_template_flagicon(template: mwp.nodes.template.Template) -> bool:
    return template.name.strip().lower() in FLAG_ICON_TEMPLATE_NAMES

def ubli_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    return ubl_to_list(mwp.parse(str(commander_code).replace("{{ubli|", "{{ubl|")))

def unbulleted_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander]:
    return ubl_to_list(mwp.parse(str(commander_code).replace("unbulleted list", "ubl")))

def br_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    lst = []

    parts = [str(commander_code)]
    for br_name in BR_NAMES:
        tmp = []
        for part in parts:
            for br in part.split(br_name):
                tmp.append(br)
        parts = tmp.copy()
    for br in parts:
        lst.append(get_commander(mwp.parse(br.strip())))
    return lst

def no_list_multi_to_list(commander_code: mwp.wikicode.Wikicode) -> list[Commander | None]:
    lst = []
    lines = str(commander_code).split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        lst.append(get_commander(mwp.parse(line)))
    return lst

def get_commander(commander_code: mwp.wikicode.Wikicode) -> Commander | None:
    if not commander_code or str(commander_code).strip() == "":
        logging.warning("Empty commander code")
        return None

    # Skip nowrap template
    if commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap"):
        commander_code = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap")[0].get(1).value

    # Skip ill template
    if commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "ill"):
        commander_code = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "ill")[0].get(1).value

    commander = Commander(None, None)

    commander_multi_allegiance = False

    code_for_logs = str(commander_code)
    for temp in commander_code.filter_templates():
        if temp.name.strip().lower() in ["flagicon", "flagdeco"]:
            country_name = temp.get(1).value.strip_code().strip()
            if commander.allegiance:
                commander_multi_allegiance = True
            commander.allegiance = Country(name=country_name)
            commander_code.remove(temp)

    
    wikilinks = commander_code.filter_wikilinks()
    if wikilinks and len(wikilinks) == 1:
        commander.name = wikilinks[0].title.strip_code().strip()
    else:
        logging.warning("No single wikilink found for commander, using stripped code as name. Wikicode: %s", code_for_logs)
        clean_name = commander_code.strip_code().strip()

        if clean_name == "?":
            logging.warning("Commander name is a '?', setting commander to None. Wikicode: %s", code_for_logs)
            return None
        elif "?" in clean_name:
            print(clean_name)

        if clean_name and len(clean_name) > 1:
            commander.name = clean_name

    if wikilinks and len(wikilinks) > 1:
        logging.warning("Detected multiple wikilinks in commander code, there could be a better naming. Wikicode: %s", code_for_logs)
    if commander_multi_allegiance:
        if commander.name in MULTI_ALLEGIANCE_COMMANDER_NAMES:
            logging.warning("Detected commander with multiple allegiances, it's a known case (%s)", (commander.name))
        else:
            logging.error("Detected commander with multiple allegiances (%s). Wikicode: %s", commander.name, code_for_logs)

    if not commander.name:
        logging.error("Commander has no name. Wikicode: %s", code_for_logs)
    return commander