from comnet.visualizer.plotter import save_graph_as_img
from comnet.visualizer.utils import get_color_dict, get_commanders_from_csv, get_edges_from_csv
import networkx as nx

def save_ww1_graph(output_file: str = "data/visualized/ww1_graph.png"):
    edges = get_edges_from_csv("data/normalized/battles.csv")
    g = nx.Graph()
    g.add_edges_from(edges)

    colors = get_color_dict(get_commanders_from_csv("data/normalized/commanders.csv"))

    countries = set()
    for commander in get_commanders_from_csv("data/normalized/commanders.csv"):
        countries.add(commander.country)

    save_graph_as_img(g, colors, output_file)

def main():
    print("Visualizing...")
    save_ww1_graph()

if __name__ == "__main__":
    main()