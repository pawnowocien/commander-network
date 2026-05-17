import os

import matplotlib.pyplot as plt
import networkx as nx

def save_graph_as_img(g, colors = None, output_file: str = "data/visualized/graph.png"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.figure(figsize=(35, 35))
    pos = nx.spring_layout(g)

    if colors:
        _colors = [colors.get(node, "gray") for node in g.nodes()]
        nx.draw(g, pos, with_labels=True, node_color=_colors, edge_color="gray", node_size=350, linewidths=1, edgecolors="black", font_size=8)
    else:
        nx.draw(g, pos, with_labels=False, edge_color="gray", node_size=50, linewidths=1, edgecolors="black")

    plt.savefig(output_file)
    plt.close()