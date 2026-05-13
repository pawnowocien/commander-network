from dataclasses import asdict
import logging

from comnet.parser.models import ParseBattle
from comnet.parser.parser import parse_files


def test_():
    battles = parse_files()
    _dict = [asdict(battle) for battle in battles]

    battles2 = [ParseBattle.from_dict(battle) for battle in _dict]


    assert battles == battles2