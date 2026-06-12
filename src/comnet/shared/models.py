from dataclasses import dataclass

from comnet.shared.consts import WIKI_PREFIX

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

    def __lt__(self, other):
        if not isinstance(other, Commander):
            return NotImplemented
        return self.name < other.name
    
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
    




@dataclass(frozen=True)
class BattleRow:
    name: str
    commander1: str
    commander2: str

    @staticmethod
    def from_csv(line: str):
        parts = line.strip().split(";")
        if len(parts) != 3:
            raise ValueError(f"Invalid line format: {line}")
        return BattleRow(name=parts[0], commander1=parts[1], commander2=parts[2])


@dataclass(frozen=True)
class CommanderRow:
    name: str
    country: str

    @staticmethod
    def from_csv(line: str):
        parts = line.strip().split(";")
        return CommanderRow(name=parts[0], country=parts[1])