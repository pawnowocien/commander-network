import os

import networkx as nx

from comnet.visualizer.analysis_centrality import run_centrality_analysis
from comnet.visualizer.analysis_community import run_predictions
from comnet.visualizer.analysis_triads import closed_triad_types, count_triads, open_triad_types
from comnet.visualizer.const import VIZ_DIR
from comnet.visualizer.plotter import save_centrality_stats, save_communities_stats, save_graph_as_img, save_triad_stats
from comnet.visualizer.utils import get_com_to_col, remove_small_components


def do_full_analysis(allies_edges: set[tuple[str, str, int]], enemies_edges: set[tuple[str, str, int]], com_to_country, country_to_col):

    # Generate all


    G_allies = nx.Graph()
    G_allies.add_weighted_edges_from(allies_edges)

    G_full = nx.Graph()
    G_full.add_weighted_edges_from(allies_edges)
    G_full.add_weighted_edges_from(enemies_edges)

    G_allies, pos_allies = _show_and_cut(G_allies, com_to_country, country_to_col, name="allies")
    G_full, pos_full = _show_and_cut(G_full, com_to_country, country_to_col, name="all")


    # Community detection

    _do_community_analysis(G_allies, com_to_country, country_to_col, pos_allies, name="allies")
    _do_community_analysis(G_full, com_to_country, country_to_col, pos_full, name="all")


    # Triads analysis

    _do_triads_analysis(set((e[0], e[1]) for e in allies_edges), set((e[0], e[1]) for e in enemies_edges), com_to_country)


    # Centrality measures

    _do_centrality_analysis(G_allies, com_to_country, country_to_col, name="allies")
    _do_centrality_analysis(G_full, com_to_country, country_to_col, name="full")


def _show_and_cut(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], name: str) -> tuple[nx.Graph, dict]:
    pos = nx.spring_layout(G, weight='weight')
    save_graph_as_img(G, colors=get_com_to_col(com_to_country, country_to_col), output_file=f"{VIZ_DIR}{name}_full", weights=True, pos=pos)
    G_cut = remove_small_components(G, min_size=10)
    save_graph_as_img(G_cut, colors=get_com_to_col(com_to_country, country_to_col), output_file=f"{VIZ_DIR}{name}_cut", weights=True, pos=pos)

    return G_cut, pos





def _do_community_analysis(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], pos: dict, name: str):
    scores = run_predictions(G, get_com_to_col(com_to_country, country_to_col), pos=pos, output_path=f"{VIZ_DIR}communities/{name}")
    save_communities_stats(scores, f"{VIZ_DIR}communities/{name}_stats.png")



def _do_triads_analysis(allies: set[tuple[str, str]], enemies: set[tuple[str, str]], com_to_country: dict[str, str]):
    os.makedirs(f"{VIZ_DIR}triads/", exist_ok=True)

    count, _ = open_triad_types(allies, enemies)
    save_triad_stats(count, f"{VIZ_DIR}triads/open_triad_stats.png")

    count, exceptions = closed_triad_types(allies, enemies)
    save_triad_stats(count, f"{VIZ_DIR}triads/closed_triad_stats.png")

    with open(f"{VIZ_DIR}triads/exceptions.txt", "w", encoding="utf-8") as f:
        for u, v in exceptions:
            f.write(f"{u} ({com_to_country.get(u, 'Unknown')}) vs {v} ({com_to_country.get(v, 'Unknown')})\n")


def _do_centrality_analysis(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], name: str):
    centrality_scores = run_centrality_analysis(G)

    for centrality, scores in centrality_scores.items():
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        save_centrality_stats(list((d[1], d[0]) for d in sorted_scores),
                              com_to_country, country_to_col, f"{VIZ_DIR}centrality/{name}_{centrality}.png", name=centrality)
