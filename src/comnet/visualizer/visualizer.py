from comnet.normalizer.consts.country_dict import COUNTRY_TO_COLOR
from comnet.visualizer.analysis_community import predict_communities
from comnet.visualizer.analysis_triads import analyse_triads
from comnet.visualizer.full_analysis import do_full_analysis
from comnet.visualizer.plotter import colors_from_sets, save_edges_as_img, save_graph_as_img
from comnet.visualizer.utils import get_allies_edges_w, get_color_dict, get_com_to_country, get_commanders_from_csv, get_enemies_edges_w
import networkx as nx

# def create_normal_vis():
#     allies = get_allies_edges_w()
#     enemies = get_enemies_edges_w()

#     commanders = get_commanders_from_csv("data/normalized/commanders.csv")
#     color_dict = get_color_dict(commanders)

#     G = nx.Graph()
#     G.add_weighted_edges_from(allies)
#     # G.add_weighted_edges_from(enemies)

#     # save_edges_as_img(allies, enemies, colors=color_dict, output_file="data/visualized/graph.png", weights=True)
#     save_graph_as_img(G, colors=color_dict, output_file="data/visualized/graph.png", weights=True)


def main():
    allies = get_allies_edges_w()
    enemies = get_enemies_edges_w()
    do_full_analysis(allies, enemies, get_com_to_country("data/normalized/commanders.csv"), COUNTRY_TO_COLOR)
    # print("Visualizing...")
    # predict_communities()
    # analyse_triads()

if __name__ == "__main__":
    main()