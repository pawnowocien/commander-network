import networkx as nx

from comnet.normalizer.consts.country_dict import COUNTRY_TO_REGION
from comnet.visualizer.plotter import colors_from_sets, save_graph_as_img
from comnet.visualizer.utils import get_color_dict, get_color_dict_region, get_commanders_from_csv, get_edges_from_csv, remove_small_components


def predict_communities(output_dir: str = "data/visualized/ww1/community/"):
    commanders = get_commanders_from_csv("data/normalized/commanders.csv")
    colors_countries = get_color_dict(commanders)
    colors_regions = get_color_dict_region(commanders)


    edges = get_edges_from_csv("data/normalized/battles.csv")
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)

    save_graph_as_img(G, colors_countries, f"{output_dir}countries.png", pos=pos)
    save_graph_as_img(G, colors_regions, f"{output_dir}regions.png", pos=pos)


    G_cut = remove_small_components(G)
    pos = nx.spring_layout(G_cut, seed=42)

    save_graph_as_img(G_cut, colors_countries, f"{output_dir}countries_cut.png", pos=pos)
    save_graph_as_img(G_cut, colors_regions, f"{output_dir}regions_cut.png", pos=pos)


    guessed_communities = nx.community.greedy_modularity_communities(G_cut)
    colors_communities = colors_from_sets(guessed_communities)
    save_graph_as_img(G_cut, colors_communities, f"{output_dir}communities_cut.png", pos=pos)

if __name__ == "__main__":
    predict_communities()