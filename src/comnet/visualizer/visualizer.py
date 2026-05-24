from comnet.visualizer.analysis_community import predict_communities
from comnet.visualizer.analysis_triads import analyse_triads
from comnet.visualizer.plotter import colors_from_sets, save_graph_as_img
from comnet.visualizer.utils import get_color_dict, get_color_dict_region, get_commanders_from_csv, get_edges_from_csv
import networkx as nx




def main():
    # print("Visualizing...")
    # predict_communities()
    analyse_triads()

if __name__ == "__main__":
    main()