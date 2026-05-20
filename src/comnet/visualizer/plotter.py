import os

import matplotlib.pyplot as plt
import matplotlib.colors as clr
import networkx as nx


def save_graph_as_img(G, colors = None, output_file: str = "data/visualized/graph.png", show_labels: bool = False, pos=None):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fig, ax = plt.subplots(figsize=(25, 25))

    if pos is None:
        pos = nx.spring_layout(G)

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color="black",
        alpha=0.4
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