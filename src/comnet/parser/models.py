from enum import Enum

from dataclasses import dataclass, field

from comnet.shared.consts import WIKI_PREFIX

@dataclass
class ParseCountry:
    name: str

    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def from_dict(data: dict) -> "ParseCountry":
        return ParseCountry(name=data['name'])

@dataclass
class ParseCommander:
    name: str
    allegiance: list[ParseCountry] = field(default_factory=list)

    def __str__(self) -> str:
        if self.allegiance:
            return f"{self.name} ({', '.join([country.name for country in self.allegiance])})"
        return self.name

    @staticmethod
    def from_dict(data: dict) -> "ParseCommander":
        return ParseCommander(
            name=data['name'],
            allegiance=[ParseCountry.from_dict(country) for country in data['allegiance']]
        )

@dataclass
class ParseSide:
    countries: list[ParseCountry] = field(default_factory=list)
    commanders: list[ParseCommander] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "ParseSide":
        return ParseSide(
            countries=[ParseCountry.from_dict(country) for country in data['countries']],
            commanders=[ParseCommander.from_dict(commander) for commander in data['commanders']]
        )

@dataclass
class ParseBattle:
    raw_name: str

    name: str
    sides: list[ParseSide] = field(default_factory=list)

    def _list_to_str(self, lst: list[ParseCountry] | list[ParseCommander], indent: int = 4) -> str:
        if not lst:
            return " " * indent + "None"
        else:
            res = ""
            for item in lst:
                res += " " * indent + str(item) + "\n"
            return res[:-1]

    def __str__(self) -> str:
        res = f"{self.name}:\n"
        for side in self.sides:
            res += f"{self._list_to_str(side.countries)}\n"
            res += f"{self._list_to_str(side.commanders, 8)}\n"
        return res
    
    def get_link(self) -> str:
        return WIKI_PREFIX + self.raw_name
    
    @staticmethod
    def from_dict(data: dict) -> "ParseBattle":
        return ParseBattle(
            raw_name=data['raw_name'],
            name=data['name'],
            sides=[
                ParseSide(
                    countries=[ParseCountry.from_dict(country) for country in side['countries']],
                    commanders=[ParseCommander.from_dict(commander) for commander in side['commanders']]
                ) for side in data['sides']
            ]
        )



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