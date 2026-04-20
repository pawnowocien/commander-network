from dataclasses import dataclass
from enum import Enum


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
    UBLI = 9
    TREE_LIST = 10
    COLLAPSIBLE_LIST = 11
    PLAINLIST2 = 12