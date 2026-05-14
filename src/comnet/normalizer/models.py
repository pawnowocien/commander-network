from dataclasses import dataclass

@dataclass(frozen=True)
class BattleRow:
    name: str
    commander1: str
    commander2: str

@dataclass(frozen=True)
class CommanderRow:
    name: str
    country: str