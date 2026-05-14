from dataclasses import dataclass

from src.comnet.shared.consts import WIKI_PREFIX

@dataclass(frozen=True)
class Country:
    name: str

    def __str__(self) -> str:
        return self.name
    
    def __lt__(self, other):
        if not isinstance(other, Country):
            return NotImplemented
        return self.name < other.name

    def __le__(self, other):
        if not isinstance(other, Country):
            return NotImplemented
        return self.name <= other.name

@dataclass(frozen=True)
class Commander:
    name: str
    allegiance: Country

    def __str__(self) -> str:
        if self.allegiance:
            return f"{self.name} ({self.allegiance.name})"
        return self.name
    
@dataclass(frozen=True)
class Side:
    countries: list[Country]
    commanders: list[Commander]

@dataclass(frozen=True)
class Battle:
    raw_name: str

    name: str
    sides: list[Side]

    @staticmethod
    def _list_to_str(lst: list[Country] | list[Commander], indent: int = 4) -> str:
        if not lst:
            return " " * indent + "None"
        
        res = ""
        for item in lst:
            res += " " * indent + str(item) + "\n"
        return res[:-1]

    def get_link(self) -> str:
        return WIKI_PREFIX + self.raw_name

    def __str__(self) -> str:
        res = f"{self.name}:\n"
        for side in self.sides:
            res += f"{self._list_to_str(side.countries)}\n"
            res += f"{self._list_to_str(side.commanders, 8)}\n"
        return res