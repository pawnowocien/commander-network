from dataclasses import dataclass

@dataclass(frozen=True)
class ConfMatrix:
    tp: int
    fp: int
    tn: int
    fn: int