import itertools

import networkx as nx

from comnet.normalizer.consts.country_dict import COUNTRY_TO_REGION
from comnet.visualizer.models import ConfMatrix
from comnet.visualizer.plotter import colors_from_sets, save_graph_as_img
from comnet.visualizer.utils import get_color_dict, get_color_dict_region, get_commanders_from_csv, get_edges_from_csv, remove_small_components, sets_to_dict


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

    target = { com: colors_regions[com] for com in G_cut.nodes }
    pred = sets_to_dict(guessed_communities)
    conf_matrix = _pair_conf_matrix(target, pred)
    print(_pair_accuracy(conf_matrix))
    print(_pairwise_f1(conf_matrix))

    save_graph_as_img(G_cut, colors_communities, f"{output_dir}communities_cut.png", pos=pos)


def _pair_conf_matrix(target: dict, pred: dict) -> ConfMatrix:
    keys = set(target.keys())
    if set(pred.keys()) != keys:
        raise ValueError("Target and prediction must have the same keys.")

    tp = fp = tn = fn = 0
    pairs = itertools.combinations(keys, 2)
    for pair in pairs:
        same_target = target[pair[0]] == target[pair[1]]
        same_pred = pred[pair[0]] == pred[pair[1]]
        
        if same_target and same_pred:
            tp += 1
        elif not same_target and same_pred:
            fp += 1
        elif not same_target and not same_pred:
            tn += 1
        elif same_target and not same_pred:
            fn += 1
    return ConfMatrix(tp, fp, tn, fn)

def _pair_accuracy(mat: ConfMatrix) -> float:
    tp, fp, tn, fn = mat.tp, mat.fp, mat.tn, mat.fn
    return (tp + tn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) > 0 else 0
def _pairwise_f1(mat: ConfMatrix) -> float:
    tp, fp, fn = mat.tp, mat.fp, mat.fn
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1_score

if __name__ == "__main__":
    predict_communities()