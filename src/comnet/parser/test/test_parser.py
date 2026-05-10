import mwparserfromhell as mwp
from src.commander_network.parser.models import InvalidParse
from src.commander_network.parser.parser import parse_commander
import src.commander_network.parser.test.test_objects as test_objects


def _print_list_alt(lst: list | InvalidParse):
    if isinstance(lst, InvalidParse):
        print("Invalid parse")
        return
    for item in lst:
        print(item)
        
def test_com_pattern(wikicode: mwp.wikicode.Wikicode):
    _print_list_alt(parse_commander(wikicode))
    print("----")

if __name__ == "__main__":    
    # battles = parse_all_files()


    test_com_pattern(test_objects.com_flagicon)
    # parse_commander(test_objects.com_single_ill)
    # TODO Petsamo_expeditions.txt has two infoboxes