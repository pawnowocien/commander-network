from enum import Enum
from dataclasses import dataclass

from comnet.shared.consts import WIKI_PREFIX


@dataclass
class InvalidParse:
    def __str__(self) -> str:
        return "Invalid parse"

@dataclass (unsafe_hash=True) # TODO
class ParseCountry:
    name: str

    def __str__(self) -> str:
        return self.name

@dataclass(unsafe_hash=True) # TODO
class ParseCommander:
    name: str
    allegiance: ParseCountry | None

    def __str__(self) -> str:
        if self.allegiance:
            return f"{self.name} ({self.allegiance.name})"
        return self.name

@dataclass
class ParseBattle:
    raw_name: str

    name: str | InvalidParse
    side1Countries: list[ParseCountry] | InvalidParse
    side2Countries: list[ParseCountry] | InvalidParse

    side1Commanders: list[ParseCommander] | InvalidParse
    side2Commanders: list[ParseCommander] | InvalidParse

    def _list_to_str(self, lst: list[ParseCountry] | list[ParseCommander] | InvalidParse, indent: int = 4) -> str:
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
    
    def get_link(self) -> str:
        return WIKI_PREFIX + self.raw_name

class CommanderListType(Enum):
    PLAINLIST = 1
    UBL = 2
    BR = 3
    SINGLE = 4
    EMPTY = 5
    PLAINLIST_UPPER = 6
    UNBULLETED_LIST = 7
    NO_LIST_MULTI = 8
    UBLI = 9
    TREE_LIST = 10
    COLLAPSIBLE_LIST = 11
    PLAINLIST2 = 12