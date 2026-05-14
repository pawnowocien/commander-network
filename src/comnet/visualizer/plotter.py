import os

import matplotlib.pyplot as plt
import networkx as nx

def save_graph_as_img(g, colors = None, output_file: str = "data/visualized/graph.png"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(g)

    if colors:
        print(sorted(g.nodes))
        print(sorted(colors.keys()))
        _colors = [colors.get(node, "gray") for node in g.nodes()]
        nx.draw(g, pos, with_labels=False, node_color=_colors, edge_color="gray", node_size=50, linewidths=1, edgecolors="black")
    else:
        nx.draw(g, pos, with_labels=False, edge_color="gray", node_size=50, linewidths=1, edgecolors="black")

    plt.savefig(output_file)
    plt.close()