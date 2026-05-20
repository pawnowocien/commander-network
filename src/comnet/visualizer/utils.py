from comnet.normalizer.consts.country_dict import COUNTRY_TO_COLOR, COUNTRY_TO_REGION, REGION_TO_COLOR
from comnet.shared.models import BattleRow, CommanderRow
from comnet.shared.models import Commander
import networkx as nx


def get_edges_from_csv(filepath: str):
    edges = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            battle_row = BattleRow.from_csv(line)
            edges.add(_get_edge_from_battle_row(battle_row))
    return edges

def _get_edge_from_battle_row(battle_row: BattleRow):
    return tuple(sorted([battle_row.commander1, battle_row.commander2]))

def get_commanders_from_csv(filepath: str) -> list[CommanderRow]:
    commanders = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            commander_row = CommanderRow.from_csv(line)
            commanders.append(commander_row)
    return commanders


def get_color_dict(commander_rows: list[CommanderRow]) -> dict[str, str]:
    color_dict = {}
    for row in commander_rows:
        if row.country in COUNTRY_TO_COLOR:
            color_dict[row.name] = COUNTRY_TO_COLOR[row.country]
        else:
            print(f"Warning: Country {row.country} not found in COUNTRY_TO_COLOR, using default color")
            color_dict[row.name] = COUNTRY_TO_COLOR["Default"]
    return color_dict
def get_color_dict_region(commander_rows: list[CommanderRow]) -> dict[str, str]:
    color_dict = {}
    for row in commander_rows:
        region = COUNTRY_TO_REGION.get(row.country, "Other")
        if region in REGION_TO_COLOR:
            color_dict[row.name] = REGION_TO_COLOR[region]
        else:
            color_dict[row.name] = COUNTRY_TO_COLOR.get(row.country, COUNTRY_TO_COLOR["Default"])
            
    return color_dict


def remove_small_components(G, min_size=5) -> nx.Graph:
    G_res = G.copy()
    components = list(nx.connected_components(G_res))
    for component in components:
        if len(component) < min_size:
            G_res.remove_nodes_from(component)
    return G_res