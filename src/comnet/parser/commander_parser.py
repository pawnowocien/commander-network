import mwparserfromhell as mwp
from comnet.parser.consts import BR_NAMES, FLAG_ICON_TEMPLATE_NAMES, RANK_WIKILINKS_TO_REMOVE
from .models import InvalidParse, ParseCommander, ParseCountry, CommanderListType
import logging
import re


def parse_commander(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander] | InvalidParse:
    commanders = []
    match _get_commander_list_type(commander_code):
        case CommanderListType.PLAINLIST:
            logging.info("Detected plainlist commander format")
            commanders = _plainlist_to_list(commander_code)
        case CommanderListType.PLAINLIST2:
            logging.info("Detected Plain list commander format")
            commanders = _plainlist2_to_list(commander_code)
        case CommanderListType.PLAINLIST_UPPER:
            logging.info("Detected Plainlist commander format")
            commanders = _plainlist_upper_to_list(commander_code)
        case CommanderListType.TREE_LIST:
            logging.info("Detected tree list commander format")
            commanders = _tree_list_to_list(commander_code)
        case CommanderListType.COLLAPSIBLE_LIST:
            logging.info("Detected collapsible list commander format")
            commanders = _collapsible_list_to_list(commander_code)
        case CommanderListType.UBL:
            logging.info("Detected ubl commander format")
            commanders = _ubl_to_list(commander_code)
        case CommanderListType.UBLI:
            logging.info("Detected ubli commander format")
            commanders = _ubli_to_list(commander_code)
        case CommanderListType.UNBULLETED_LIST:
            logging.info("Detected unbulleted list commander format")
            commanders = _unbulleted_to_list(commander_code)
        case CommanderListType.BR:
            logging.info("Detected br commander format")
            commanders = _br_to_list(commander_code)
        case CommanderListType.SINGLE:
            logging.info("Detected single commander format")
            commanders = [_get_commander(commander_code)]
        case CommanderListType.NO_LIST_MULTI:
            logging.info("Detected no-list multi-line commander format")
            commanders = _no_list_multi_to_list(commander_code)
        case CommanderListType.EMPTY:
            logging.warning("Detected empty commander format")
            return []
        case None:
            logging.error("Could not determine commander list type for code: %s", commander_code)
            return InvalidParse()
        case _:
            logging.error("Unhandled commander list type for code: %s", commander_code)
            return InvalidParse()
    
    return _clear_list(commanders)

def _clear_list(commander_list: list[ParseCommander | None]) -> list[ParseCommander]:
    lst = []
    for commander in commander_list:
        if commander:
            lst.append(commander)
    return lst

def _get_commander_list_type(commander_code: mwp.wikicode.Wikicode) -> CommanderListType | None:
    for node in commander_code.nodes:
        templates = mwp.parse(str(node)).filter_templates()
        if not templates:
            if _contains_br(node):
                return CommanderListType.BR
            continue

        if templates[0].name.strip() == "plainlist":
            return CommanderListType.PLAINLIST
        if templates[0].name.strip() == "Plain list":
            return CommanderListType.PLAINLIST2
        elif templates[0].name.strip() == "Plainlist":
            return CommanderListType.PLAINLIST_UPPER
        elif templates[0].name.strip() == "Collapsible list":
            return CommanderListType.COLLAPSIBLE_LIST
        elif templates[0].name.strip().lower() == "tree list":
            return CommanderListType.TREE_LIST
        elif templates[0].name.strip().lower() == "ubl":
            return CommanderListType.UBL
        elif templates[0].name.strip().lower() == "ubli":
            return CommanderListType.UBLI
        elif templates[0].name.strip().lower() == "unbulleted list":
            return CommanderListType.UNBULLETED_LIST
        elif _contains_br(node):
            return CommanderListType.BR
    
    stripped_code = str(commander_code).strip()

    if len(stripped_code) == 0 or stripped_code == "|":
        return CommanderListType.EMPTY
    
    if stripped_code.count("\n") == 0:
        return CommanderListType.SINGLE
    else:
        return CommanderListType.NO_LIST_MULTI

def _contains_br(node: mwp.nodes.Node) -> bool:
    for br_name in BR_NAMES:
        if br_name in str(node):
            return True
    return False

def _plainlist_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
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

        lst.append(_get_commander(mwp.parse(line)))

    return lst

def _plainlist2_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    commander_str = str(commander_code)
    commander_str = commander_str.replace("{{Plain list|", "{{plainlist|")
    return _plainlist_to_list(mwp.parse(commander_str))

def _plainlist_upper_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    commander_str = str(commander_code)
    commander_str = commander_str.replace("{{Plainlist}}", "{{plainlist|")
    commander_str = commander_str.replace("{{Endplainlist}}", "}}")
    return _plainlist_to_list(mwp.parse(commander_str))

def _tree_list_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    commander_str = str(commander_code)
    commander_str = commander_str.replace("{{tree list}}", "{{plainlist|")
    commander_str = commander_str.replace("{{tree list/end}}", "}}")
    return _plainlist_to_list(mwp.parse(commander_str))

def _collapsible_list_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    code = ""
    for part in str(commander_code).split("\n"):
        if "{{Collapsible list" in part:
            code += part.replace("{{Collapsible list", "{{plainlist|") + "\n"
        elif part.strip().startswith("|"):
            if part[1:].strip().startswith(("title", "bullets")):
                continue
            code += "* " + part[1:] + "\n"
        elif part.strip() == "}}":
            code += "}}"
    return _plainlist_to_list(mwp.parse(code))

def _ubl_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    lst = []

    current_code = ""
    for node in commander_code.nodes:
        current_code += str(node)
        if isinstance(node, mwp.nodes.Template) and node.name.strip().lower() == "ubl":
            lst.extend(_single_ubl_to_list(mwp.parse(current_code)))
            current_code = ""

    return lst

def _single_ubl_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    """
    Can be either:
    - `flagicon? list[commander]`
    - `list[flagicon? commander]`
    """
    ubl_templates = _get_ubl_templates(commander_code)
    if not ubl_templates or len(ubl_templates) != 1:
        logging.error("Expected exactly one ubl template for single ubl commander format, got %d. Wikicode: %s", len(ubl_templates), commander_code)
        return []
    
    lst = []

    # flagicon? list[commander]
    if _is_template_flagicon(commander_code.filter_templates()[0]):
        country = commander_code.filter_templates()[0].get(1).value.strip_code().strip() if commander_code.filter_templates() else None
        for param in ubl_templates[0].params:
            commander = _get_commander(mwp.parse(param.value.strip()))
            if country and commander:
                commander.allegiance.append(ParseCountry(name=country))
            lst.append(commander)

    # list[flagicon? commander]
    else:
        for param in ubl_templates[0].params:
            lst.append(_get_commander(mwp.parse(param.value.strip())))
    return lst

def _get_flagicon_templates(wikicode: mwp.wikicode.Wikicode) -> list[mwp.nodes.template.Template]:
    return wikicode.filter_templates(matches=lambda t: t.name.strip().lower() in FLAG_ICON_TEMPLATE_NAMES)
def _get_ubl_templates(wikicode: mwp.wikicode.Wikicode) -> list[mwp.nodes.template.Template]:
    return wikicode.filter_templates(matches=lambda t: t.name.strip().lower() == "ubl")

def _is_template_flagicon(template: mwp.nodes.template.Template) -> bool:
    return template.name.strip().lower() in FLAG_ICON_TEMPLATE_NAMES

def _ubli_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    return _ubl_to_list(mwp.parse(str(commander_code).replace("{{ubli|", "{{ubl|")))

def _unbulleted_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    return _ubl_to_list(mwp.parse(str(commander_code).replace("unbulleted list", "ubl")))

def _br_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    lst = []

    parts = [str(commander_code)]
    for br_name in BR_NAMES:
        tmp = []
        for part in parts:
            for br in part.split(br_name):
                tmp.append(br)
        parts = tmp.copy()
    for br in parts:
        lst.append(_get_commander(mwp.parse(br.strip())))
    return lst



def _no_list_multi_to_list(commander_code: mwp.wikicode.Wikicode) -> list[ParseCommander | None]:
    lst = []

    current_chunk = mwp.wikicode.Wikicode([])
    for node in commander_code.nodes:
        if isinstance(node, mwp.nodes.Text):
            parts = node.value.split('\n')
            for i, part in enumerate(parts):
                if i > 0:
                    if str(current_chunk).strip():
                        lst.append(_get_commander(current_chunk))
                    current_chunk = mwp.wikicode.Wikicode([])
                
                if part:
                    current_chunk.append(mwp.nodes.Text(part))
        
        else:
            current_chunk.append(node)
            
    if str(current_chunk).strip():
        lst.append(_get_commander(current_chunk))
    return lst

def _get_commander(commander_code: mwp.wikicode.Wikicode) -> ParseCommander | None:
    if not commander_code or str(commander_code).strip() == "":
        logging.warning("Empty commander code")
        return None

    code_for_logs = str(commander_code)

    # Skip nowrap template
    if commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap"):
        commander_code = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "nowrap")[0].get(1).value

    # Skip ill template
    if commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "ill"):
        commander_code = commander_code.filter_templates(matches=lambda t: t.name.strip().lower() == "ill")[0].get(1).value

    for tag in commander_code.filter_tags():
        if str(tag.tag).lower() in ["ref"]:
            commander_code.remove(tag)

    # Get country

    commander = ParseCommander("", [])
    
    STATUSES_TO_REMOVE = ["kia", "wia", "mia"]
    for temp in commander_code.filter_templates():
        if _is_template_flagicon(temp):
            country_name = temp.get(1).value.strip_code().strip()
            commander.allegiance.append(ParseCountry(name=country_name))
            commander_code.remove(temp)
        elif temp.name.strip().lower() in STATUSES_TO_REMOVE:
            commander_code.remove(temp)

    for link in commander_code.filter_wikilinks():
        title = link.title.strip_code().strip().lower()
        if title.startswith(("file:", "image:")):
            filename = title.split(":", 1)[1].strip()
            commander.allegiance.append(ParseCountry(name=filename))
            commander_code.remove(link)
        
        # Handle "Petsamo_expeditions.txt" case
        elif "wounded in action" in title:
            commander_code.remove(link)

        elif title in RANK_WIKILINKS_TO_REMOVE:
            commander_code.remove(link)

    wikilinks = commander_code.filter_wikilinks()
    if wikilinks and len(wikilinks) == 1:
        commander.name = _clean_wikilink(wikilinks[0]) or ""
    else:
        logging.warning("No single wikilink found for commander, using stripped code as name. Wikicode: %s", code_for_logs)
        clean_name = _clean_corner_cases(commander_code.strip_code())
        if not clean_name:
            logging.warning("Commander name is empty after cleaning corner cases, setting commander to None. Wikicode: %s", code_for_logs)
            return None

        if clean_name in ["?", "Unknown", "Unknown officer", "unknown", "None"]:
            logging.warning("Commander name is unknown/none, setting commander to None. Wikicode: %s", code_for_logs)
            return None
        elif "?" in clean_name:
            print(clean_name)

        if clean_name and len(clean_name) > 1:
            commander.name = clean_name

    if wikilinks and len(wikilinks) > 1:
        logging.warning("Detected multiple wikilinks in commander code, there could be a better naming. Wikicode: %s", code_for_logs)

    if not commander.name:
        logging.error("Commander has no name. Wikicode: %s", code_for_logs)
    return commander



def _clean_wikilink(wikilink: mwp.nodes.wikilink.Wikilink) -> str | None:
    # Filter out :xxx: links (to other language wikis)
    INTERLANG_RE = re.compile(r"^:[a-z]{2,3}:")

    title = wikilink.title.strip_code()
    if INTERLANG_RE.match(title):
        name = wikilink.text
        if not name:
            return None
        return _clean_corner_cases(name.strip_code())
    
    return _clean_corner_cases(title)



def _clean_corner_cases(name: str) -> str | None:
    # Example - Romanian campaign (1917)
    DATE_PATTERNS = ["(from", "(until", "(after", "(before"]
    for date_pat in DATE_PATTERNS:
        if date_pat in name.lower():
            return None

    # ()        - Petsamo Expeditions (after removing WIA link)
    # '''       - Battle of the Southern Carpathians
    to_remove = ["()", "'''"]

    for item in to_remove:
        name = name.replace(item, "")
    name = name.strip()
    
    BANNED_NAMES = [
        "15th Division (North Army):", "1st Army:", "2nd Army:",            # Battle of the Southern Carpathians
        "Garrison commander:", "Among others", "Punitive force commander:", # 1916 uprising in Hilla
        "No centralized leadership",                                        # 1915 uprising in Karbala
        "Until 26 July:",                                                   # Battle of Baku
        "From 26 July:",                                                    # Battle of Baku
        "Support:",                                                         # Battle of Łowczówek
        "High Command:",                                                    # Romanian Campaign (1917)
    ]
    if name in BANNED_NAMES:
        return None
    
    if not name:
        return None
    return name