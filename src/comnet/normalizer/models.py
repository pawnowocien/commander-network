from dataclasses import dataclass

@dataclass(frozen=True)
class BattleRow:
    name: str
    commander1: str
    commander2: str

    @staticmethod
    def from_csv(line: str):
        parts = line.strip().split(",")
        return BattleRow(name=parts[0], commander1=parts[1], commander2=parts[2])


@dataclass(frozen=True)
class CommanderRow:
    name: str
    country: str

    @staticmethod
    def from_csv(line: str):
        parts = line.strip().split(",")
        return CommanderRow(name=parts[0], country=parts[1])