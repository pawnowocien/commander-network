import os

import matplotlib.pyplot as plt
import networkx as nx

def save_graph_as_img(g, colors = None, output_file: str = "data/visualized/graph.png", show_labels: bool = False):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fig, ax = plt.subplots(figsize=(25, 25))

    pos = nx.spring_layout(g)

    nx.draw_networkx_edges(
        g,
        pos,
        ax=ax,
        edge_color="black",
        alpha=0.4
    )

    node_color = [colors.get(node, "gray") for node in g.nodes()] if colors else "gray"
    nx.draw_networkx_nodes(
        g,
        pos,
        ax=ax,
        node_size=300,
        alpha=0.8,
        edgecolors="black",
        node_color=node_color,
        linewidths=1
    )

    if show_labels:
        nx.draw_networkx_labels(g, pos, ax=ax, font_size=8)

    ax.set_axis_off()
    fig.savefig(output_file, bbox_inches="tight")
    plt.close()