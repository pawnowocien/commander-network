import os

import matplotlib.pyplot as plt
import networkx as nx

def save_graph_as_img(g, colors = None, output_file: str = "data/visualized/graph.png", show_labels: bool = False):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.figure(figsize=(30, 30))
    pos = nx.spring_layout(g)

    nx.draw_networkx_edges(
        g,
        pos,
        edge_color="black",
        alpha=0.4
    )

    node_color = [colors.get(node, "gray") for node in g.nodes()] if colors else "gray"
    nx.draw_networkx_nodes(
        g,
        pos,
        node_size=100,
        edgecolors="black",
        node_color=node_color,
        linewidths=1
    )

    if show_labels:
        nx.draw_networkx_labels(g, pos, font_size=8)

    # if colors:
    #     _colors = [colors.get(node, "gray") for node in g.nodes()]
    #     nx.draw(g, pos, with_labels=show_labels, node_color=_colors, edge_color="gray", node_size=350, linewidths=1, edgecolors="black", font_size=8)
    # else:
    #     nx.draw(g, pos, with_labels=show_labels, edge_color="gray", node_size=50, linewidths=1, edgecolors="black")

    plt.savefig(output_file)
    plt.close()