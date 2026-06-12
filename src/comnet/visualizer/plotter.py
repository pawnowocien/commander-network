import os

import matplotlib.pyplot as plt
import matplotlib.colors as clr
import networkx as nx

from comnet.visualizer.const import VIZ_DIR
from comnet.visualizer.utils import get_com_to_col


def save_graph_as_img(G, colors = None, output_file: str = f"{VIZ_DIR}graph.png", show_labels: bool = False, pos=None, weights=False):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fig, ax = plt.subplots(figsize=(25, 25))

    if pos is None:
        pos = nx.spring_layout(G, weight='weight' if weights else None)

    if weights:
        max_weight = max((G[u][v]['weight'] for u, v in G.edges()), default=1)
        edge_widths = [20 * G[u][v]['weight'] / max_weight for u, v in G.edges()]
    else:
        edge_widths = 1

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color="black",
        alpha=0.4,
        width=edge_widths
    )

    node_color = [colors.get(node, "gray") for node in G.nodes()] if colors else "gray"
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=300,
        alpha=0.8,
        edgecolors="black",
        node_color=node_color,
        linewidths=1
    )

    if show_labels:
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

    ax.set_axis_off()
    fig.savefig(output_file, bbox_inches="tight")
    plt.close()

def colors_from_sets(sets):
    color_dict = {}
    for i, s in enumerate(sets):
        color = list(clr.TABLEAU_COLORS.values())[i % len(clr.TABLEAU_COLORS)]
        for node in s:
            color_dict[node] = color
    return color_dict





def save_edges_as_img(allies: set[tuple], enemies: set[tuple], colors = None, output_file: str = f"{VIZ_DIR}edges.png",
                      pos=None, weights=False):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fig, ax = plt.subplots(figsize=(25, 25))

    G = nx.Graph()
    if weights:
        G.add_weighted_edges_from(allies)
        G.add_weighted_edges_from(enemies)
    else:
        G.add_edges_from(allies)
        G.add_edges_from(enemies)

    if pos is None:
        if weights:
            tmp_G = nx.Graph()
            tmp_G.add_weighted_edges_from(allies)
            tmp_G.add_nodes_from(G.nodes())
            pos = nx.spring_layout(tmp_G, weight='weight')
        else:
            pos = nx.spring_layout(G)



    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=allies,
        ax=ax,
        edge_color="gray",
        alpha=0.8,
        width=1
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=enemies,
        ax=ax,
        edge_color="darkred",
        alpha=0.05,
        width=1
    )


    node_color = [colors.get(node, "gray") for node in G.nodes()] if colors else "gray"
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=300,
        alpha=0.8,
        edgecolors="black",
        node_color=node_color,
        linewidths=1
    )

    ax.set_axis_off()
    fig.savefig(output_file, bbox_inches="tight")
    plt.close()






def save_communities_stats(stats: dict[str, dict[str, float]], output_file: str):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    scores = {}

    for graph_type, graph_stats in stats.items():
        for method, score in graph_stats.items():
            if not method in scores.keys():
                scores[method] = []
            scores[method].append((score, graph_type))

    for method, scores in scores.items():
        _save_single_community_stat(method, scores, f"{output_file}_{method}.png")

def _save_single_community_stat(measure_name: str, scores: list[tuple[float, str]], output_file: str):
    values = [s[0] for s in scores]
    labels = [s[1] for s in scores]

    assert labels == ["random", "greedy", "louvain", "label_prop"]
    colors = ['slategray', 'goldenrod', 'royalblue', 'brown']

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(labels, values, color=colors)
    ax.set_xlabel('Detection Method')
    ax.set_ylabel('Score')
    ax.set_title(f'{measure_name.replace("_", " ").capitalize()} by Detection Method')

    plt.tight_layout()
    fig.savefig(output_file)
    plt.close()



def save_triad_stats(stats: dict[int, int], output_file: str):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    assert set(stats.keys()) == {0, 1, 2} or set(stats.keys()) == {0, 1, 2, 3}

    if set(stats.keys()) == {0, 1, 2}:
        title = "Open Triads"
        new_stats = {
            "- -": stats[0],
            "+ -": stats[1],
            "+ +": stats[2],
        }
        colors = ['firebrick', 'goldenrod', 'forestgreen']
    else:
        title = "Closed Triads"
        new_stats = {
            "- - -": stats[0],
            "+ - -": stats[1],
            "+ + -": stats[2],
            "+ + +": stats[3]
        }
        colors = ['firebrick', 'indianred', 'yellowgreen', 'forestgreen']


    fig, ax = plt.subplots(figsize=(10, 5))

    _sum = sum(new_stats.values())
    frac_values = [v / _sum for v in new_stats.values()]

    bar_container = ax.bar(list(new_stats.keys()), frac_values, color=colors)
    ax.bar_label(bar_container, labels=[f"{v:,}" for v in new_stats.values()], padding=3)
    ax.set_ylim(0, 1)

    ax.set_xlabel('Triad type')
    ax.set_ylabel('Fraction')
    ax.set_title(title)

    plt.tight_layout()
    fig.savefig(output_file)
    plt.close()










def save_centrality_stats(stats: list[tuple[float, str]], com_to_country: dict[str, str], country_to_col: dict[str, str], output_file: str, name: str):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    values = [s[0] for s in stats[:20]][::-1]
    labels = [s[1] for s in stats[:20]][::-1]

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = [get_com_to_col({label: com_to_country.get(label, "Unknown")}, country_to_col).get(label, "gray") for label in labels]
    ax.barh(labels, values, color=colors)

    ax.set_xlim(0, max(values) * 1.1)

    ax.set_xlabel(f'Centrality Score')
    ax.set_ylabel('Commander')
    ax.set_title(f'{name.capitalize()} Centrality')

    plt.tight_layout()
    fig.savefig(output_file)
    plt.close()
