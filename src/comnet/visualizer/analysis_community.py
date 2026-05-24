import itertools
import random

import networkx as nx

from comnet.normalizer.consts.country_dict import COUNTRY_TO_REGION
from comnet.visualizer.models import ConfMatrix
from comnet.visualizer.plotter import colors_from_sets, save_graph_as_img
from comnet.visualizer.utils import get_color_dict, get_color_dict_region, get_commanders_from_csv, get_edges_from_csv, remove_small_components, sets_to_dict


def predict_communities(output_dir: str = "data/visualized/ww1/community/"):
    commanders = get_commanders_from_csv("data/normalized/commanders.csv")
    colors_countries = get_color_dict(commanders)
    colors_regions = get_color_dict_region(commanders)

    allies = get_edges_from_csv("data/normalized/battles_allies.csv")
    enemies = get_edges_from_csv("data/normalized/battles_enemies.csv")
    G = nx.Graph()
    G.add_edges_from(allies)
    G.add_edges_from(enemies)

    scores = _run_analysis(G, colors_countries, colors_regions, f"{output_dir}full/")
    _pretty_print("Original graph scores", scores)

    G_cut = remove_small_components(G)
    scores = _run_analysis(G_cut, colors_countries, colors_regions, f"{output_dir}cut/")
    _pretty_print("\nCut graph scores", scores)

def _run_analysis(G: nx.Graph, colors_countries: dict, 
                  colors_regions: dict, output_path: str) -> dict[str, dict[str, dict[str, float]]]:
    pos = nx.spring_layout(G, seed=42)
    scores = {}

    scores['countries'] = _run_predictions(G, colors_countries, pos, f"{output_path}countries_pred_")
    save_graph_as_img(G, colors_countries, f"{output_path}countries.png", pos=pos)

    scores['regions'] = _run_predictions(G, colors_regions, pos, f"{output_path}regions_pred_")
    save_graph_as_img(G, colors_regions, f"{output_path}regions.png", pos=pos)

    return scores

def _run_predictions(G: nx.Graph, colors: dict, pos: dict, output_path: str) -> dict[str, dict[str, float]]:
    n_communities = len(set(colors.values()))

    scores = {}

    random_guessed = [set() for _ in range(n_communities)]
    for node in G.nodes:
        random_guessed[random.randint(0, n_communities - 1)].add(node)
    random_colors = colors_from_sets(random_guessed)
    save_graph_as_img(G, random_colors, f"{output_path}random.png", pos=pos)
    scores['random'] = _evaluate_prediction(G, colors, random_guessed)

    greedy_guessed = nx.community.greedy_modularity_communities(G)
    greedy_colors = colors_from_sets(greedy_guessed)
    save_graph_as_img(G, greedy_colors, f"{output_path}greedy.png", pos=pos)
    scores['greedy'] = _evaluate_prediction(G, colors, greedy_guessed)

    louvain_guessed = nx.community.louvain_communities(G, seed=42)
    louvain_colors = colors_from_sets(louvain_guessed)
    save_graph_as_img(G, louvain_colors, f"{output_path}louvain.png", pos=pos)
    scores['louvain'] = _evaluate_prediction(G, colors, louvain_guessed)

    label_prop_guessed = nx.community.label_propagation_communities(G)
    label_prop_colors = colors_from_sets(label_prop_guessed)
    save_graph_as_img(G, label_prop_colors, f"{output_path}label_prop.png", pos=pos)
    scores['label_prop'] = _evaluate_prediction(G, colors, label_prop_guessed)

    return scores

def _evaluate_prediction(G: nx.Graph, colors: dict, guessed_communities: list) -> dict[str, float]:
    target = { com: colors[com] for com in G.nodes }
    pred = sets_to_dict(guessed_communities)
    conf_matrix = _pair_conf_matrix(target, pred)
    return {
        "accuracy": _pair_accuracy(conf_matrix),
        "f1_score": _pairwise_f1(conf_matrix)
    }

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


def _pretty_print(section: str, scores: dict[str, dict[str, dict[str, float]]]):
    print(f"{section}:")
    for graph_type, preds in scores.items():
        print(f"{graph_type}:")
        for pred_type, metrics in preds.items():
            for metric, score in metrics.items():
                print(f"\t{pred_type} - {metric}: {score:.4f}")

if __name__ == "__main__":
    predict_communities()