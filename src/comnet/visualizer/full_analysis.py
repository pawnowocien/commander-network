import os

from matplotlib import pyplot as plt
import networkx as nx
import json

from comnet.visualizer.analysis_centrality import run_centrality_analysis
from comnet.visualizer.analysis_community import run_predictions
from comnet.visualizer.analysis_triads import closed_triad_types, open_triad_types
from comnet.visualizer.const import VIZ_DIR
from comnet.visualizer.plotter import make_community_pie_chart, make_plot_on_ax, make_unbalanced_pie_chart, save_centrality_stats, save_communities_stats, save_graph_as_img, save_triad_stats
from comnet.visualizer.utils import get_com_to_col, remove_small_components
from comnet.config import pipeline_type
from comnet.visualizer.basic_stats import analyze_basic_stats


def do_full_analysis(allies_edges: set[tuple[str, str, int]], enemies_edges: set[tuple[str, str, int]], com_to_country, country_to_col):

    # Generate all


    G_allies = nx.Graph()
    G_allies.add_weighted_edges_from(allies_edges)
    

    G_full = nx.Graph()
    G_full.add_weighted_edges_from(allies_edges)
    G_full.add_weighted_edges_from(enemies_edges)


    # Basic stats before cutting small components

    _save_basic_stats(G_allies, com_to_country, name="positive")
    _save_basic_stats(G_full, com_to_country, name="full")

    G_allies_all = G_allies.copy()
    G_full_all = G_full.copy()
    G_allies, pos_allies = _show_and_cut(G_allies, com_to_country, country_to_col, name="positive")
    G_full, pos_full = _show_and_cut(G_full, com_to_country, country_to_col, name="full")


    # Show all

    _show_all(G_allies_all, G_full_all, G_allies, G_full, get_com_to_col(com_to_country, country_to_col), pos_allies, pos_full, name="all_comparison")


    # Basic stats

    _save_basic_stats(G_allies, com_to_country, name="positive_cut")
    _save_basic_stats(G_full, com_to_country, name="full_cut")

    basic_stats_dir = f"{VIZ_DIR}basic_stats/"
    all_paths = (f"{basic_stats_dir}full_stats.json", f"{basic_stats_dir}full_cut_stats.json")
    positive_paths = (f"{basic_stats_dir}positive_stats.json", f"{basic_stats_dir}positive_cut_stats.json")
    _create_latex_table(all_paths, positive_paths)


    # Community detection

    _do_community_analysis(G_allies, com_to_country, country_to_col, pos_allies, name="positive")
    _do_community_analysis(G_full, com_to_country, country_to_col, pos_full, name="full")


    # Triads analysis

    _do_triads_analysis(set((e[0], e[1]) for e in allies_edges), set((e[0], e[1]) for e in enemies_edges), 
                        com_to_country, country_to_col)


    # Centrality measures

    _do_centrality_analysis(G_allies, com_to_country, country_to_col, name="positive")
    _do_centrality_analysis(G_full, com_to_country, country_to_col, name="full")


def _show_and_cut(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], name: str) -> tuple[nx.Graph, dict]:
    pos = nx.spring_layout(G, weight='weight')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(50, 25))
    
    colors = get_com_to_col(com_to_country, country_to_col)

    make_plot_on_ax(G, ax1, colors, pos=pos, weights=True, title=f"Full graph ({pipeline_type.upper()} {name})")
    G_cut = remove_small_components(G, min_size=10)
    make_plot_on_ax(G_cut, ax2, colors, pos=pos, weights=True, title=f"Cut graph ({pipeline_type.upper()} {name})")

    os.makedirs(VIZ_DIR, exist_ok=True)
    plt.savefig(f"{VIZ_DIR}{name}", bbox_inches="tight")


    return G_cut, pos





def _do_community_analysis(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], pos: dict, name: str):
    scores, colors, communities = run_predictions(G, get_com_to_col(com_to_country, country_to_col), 
                                                  pos=pos, output_path=f"{VIZ_DIR}communities/{name}")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(60, 40), layout="constrained")

    make_plot_on_ax(G, ax1, get_com_to_col(com_to_country, country_to_col), pos=pos, title="Ground Truth")
    make_plot_on_ax(G, ax2, colors['greedy'], pos=pos, title="Clauset-Newman-Moore")
    make_plot_on_ax(G, ax3, colors['louvain'], pos=pos, title="Louvain")
    make_plot_on_ax(G, ax4, colors['label_prop'], pos=pos, title="Label Propagation")

    fig.suptitle(f"Community detection comparison ({pipeline_type.upper()} {name})", fontsize=96)

    os.makedirs(f"{VIZ_DIR}communities/", exist_ok=True)
    plt.savefig(f"{VIZ_DIR}communities/{name}_communities", bbox_inches="tight")
    plt.close()


    save_communities_stats(scores, f"{VIZ_DIR}communities/{name}_stats")

    best_method = max(scores, key=lambda m: scores[m]['modularity'])
    _show_biggest_communities(communities[best_method], com_to_country, country_to_col, output_path=f"{VIZ_DIR}communities/{name}_best_communities", name=best_method)

def _show_biggest_communities(communities: list[set], com_to_country: dict[str, str], 
                              country_to_color: dict[str, str], output_path: str, name: str):
    fig_shape = (3, 3)
    fig, axs = plt.subplots(fig_shape[0], fig_shape[1], figsize=(20, 10), layout="constrained")

    communities_sorted = sorted(communities, key=lambda c: len(c), reverse=True)
    for i in range(fig_shape[0] * fig_shape[1]):
        if i < len(communities_sorted):
            community = communities_sorted[i]
            make_community_pie_chart(community, com_to_country, country_to_color, axs[i // fig_shape[1]][i % fig_shape[1]])

    plt.suptitle(f"Biggest communities in {name.capitalize()} method ({pipeline_type.upper()})", fontsize=24)
    plt.savefig(f"{output_path}.png", bbox_inches="tight")
    plt.close()


def _do_triads_analysis(allies: set[tuple[str, str]], enemies: set[tuple[str, str]], 
                        com_to_country: dict[str, str], country_to_color: dict[str, str]):
    os.makedirs(f"{VIZ_DIR}triads/", exist_ok=True)

    count, _ = open_triad_types(allies, enemies)
    save_triad_stats(count, f"{VIZ_DIR}triads/open_triad_stats.png")

    count, exceptions, unbalanced_nodes = closed_triad_types(allies, enemies)
    save_triad_stats(count, f"{VIZ_DIR}triads/closed_triad_stats.png")

    with open(f"{VIZ_DIR}triads/exceptions.txt", "w", encoding="utf-8") as f:
        for u, v in exceptions:
            f.write(f"{u} ({com_to_country.get(u, 'Unknown')}) vs {v} ({com_to_country.get(v, 'Unknown')})\n")
    
    unbalanced_countries = {}

    for u, v, w in unbalanced_nodes:
        for node in [u, v, w]:
            country = com_to_country.get(node, "Unknown")
            if country not in unbalanced_countries:
                unbalanced_countries[country] = 0
            unbalanced_countries[country] += 1
    
    make_unbalanced_pie_chart(unbalanced_nodes, com_to_country, country_to_color, f"{VIZ_DIR}triads/unbalanced_countries.png")



def _do_centrality_analysis(G: nx.Graph, com_to_country: dict[str, str], country_to_col: dict[str, str], name: str):
    centrality_scores = run_centrality_analysis(G)

    for centrality, scores in centrality_scores.items():
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        save_centrality_stats(list((d[1], d[0]) for d in sorted_scores),
                              com_to_country, country_to_col, f"{VIZ_DIR}centrality/{name}_{centrality}.png", name=centrality)


def _save_basic_stats(G: nx.Graph, com_to_country: dict[str, str], name: str):
    stats = analyze_basic_stats(G, com_to_country)
    os.makedirs(f"{VIZ_DIR}basic_stats/", exist_ok=True)

    with open(f"{VIZ_DIR}basic_stats/{name}_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)


def _create_latex_table(all_paths: tuple[str, str], coop_paths: tuple[str, str]):
    """(all_stats_path, all_cut_stats_path), (coop_stats_path, coop_cut_stats_path)"""

    all_stats = [None, None]
    coop_stats = [None, None]
    with open(all_paths[0], "r", encoding="utf-8") as f:
        all_stats[0] = json.load(f)
    with open(all_paths[1], "r", encoding="utf-8") as f:
        all_stats[1] = json.load(f)

    with open(coop_paths[0], "r", encoding="utf-8") as f:
        coop_stats[0] = json.load(f)
    with open(coop_paths[1], "r", encoding="utf-8") as f:
        coop_stats[1] = json.load(f)

    combined_dict = {}

    for key in all_stats[0].keys():
        combined_dict[key] = [all_stats[0][key], coop_stats[0][key], all_stats[1][key], coop_stats[1][key]]


    latex_string = ""
    keys_to_show = [("n_nodes", "nodes"), ("n_edges", "edges"), ("density", "density"), ("modularity", "modularity"),
                    ("n_components", "components"), ("avg_component_size", "compavg"), ("std_component_size", "compstd"), ("median_component_size", "compmed"),
                    ("n_countries", "countries"), ("avg_country_size", "countryavg"), ("std_country_size", "countrystd"), ("median_country_size", "countrymed")]

    for key, name in keys_to_show:
        values = combined_dict[key]
        values_formatted = []
        for v in values:
            if isinstance(v, float):
                if key == "density":
                    values_formatted.append(f"{v:.4f}")
                else:
                    values_formatted.append(f"{v:.2f}")
            else:
                values_formatted.append(str(v))

        lst = " & ".join(values_formatted)

        latex_string += f"  {name} = {{ {lst} }}, \n"

    latex_string = f"\\networktable{{,\n{latex_string}}}"
    print(latex_string)


def _show_all(G_allies_all: nx.Graph, G_full_all: nx.Graph, G_allies_cut: nx.Graph, G_full_cut: nx.Graph, colors: dict, pos_allies: dict, pos_full: dict, name: str):
    os.makedirs(VIZ_DIR, exist_ok=True)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(60, 40), layout="constrained")

    make_plot_on_ax(G_full_all, ax1, colors, pos=pos_full, weights=True, title=f"Full")
    make_plot_on_ax(G_allies_all, ax2, colors, pos=pos_allies, weights=True, title=f"Positive")
    make_plot_on_ax(G_full_cut, ax3, colors, pos=pos_full, weights=True, title=f"Full after cut")
    make_plot_on_ax(G_allies_cut, ax4, colors, pos=pos_allies, weights=True, title=f"Positive after cut")
    
    fig.suptitle(f"Graph comparison ({pipeline_type.upper()})", fontsize=96)

    plt.savefig(f"{VIZ_DIR}{name}", bbox_inches="tight", pad_inches=0.1)
    
    plt.close(fig) 
    return