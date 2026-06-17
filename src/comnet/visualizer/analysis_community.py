import itertools
import os
import random

from matplotlib import pyplot as plt
import networkx as nx

from comnet.visualizer.models import ConfMatrix
from comnet.visualizer.plotter import colors_from_sets, make_plot_on_ax, save_graph_as_img
from comnet.visualizer.utils import sets_to_dict


# def predict_communities(output_dir: str = "data/visualized/ww1/community/", analysis_file_path: str = "data/visualized/ww1/community/scores.txt"):
#     ANALYSIS_COUNT = 6
#     current_analysis_num = 0
#     def update_print():
#         nonlocal current_analysis_num
#         current_analysis_num +=1
#         print(f"\rDetecting communities... {current_analysis_num} / {ANALYSIS_COUNT} ", end="")
        

#     commanders = get_commanders_from_csv("data/normalized/commanders.csv")
#     colors_countries = get_color_dict(commanders)
#     colors_regions = get_color_dict_region(commanders)

#     allies = get_edges_from_csv("data/normalized/battles_allies.csv")
#     enemies = get_edges_from_csv("data/normalized/battles_enemies.csv")

#     analysis_str = ""

#     # Allies (default)
#     analysis_str += "Allied commanders\n"

#     update_print()
#     G_allies = nx.Graph()
#     G_allies.add_edges_from(allies)
#     scores = _run_analysis(G_allies, colors_countries, colors_regions, f"{output_dir}allies_full/")
#     analysis_str += _pretty_string("Original graph scores", scores)

#     update_print()
#     G_allies_cut = remove_small_components(G_allies)
#     scores = _run_analysis(G_allies_cut, colors_countries, colors_regions, f"{output_dir}allies_cut/")
#     analysis_str += _pretty_string("Cut graph scores", scores)
    
#     # Enemies
#     analysis_str += "Opposed commanders\n"

#     update_print()
#     G_enemies = nx.Graph()
#     G_enemies.add_edges_from(enemies)
#     scores = _run_analysis(G_enemies, colors_countries, colors_regions, f"{output_dir}enemies_full/")
#     analysis_str += _pretty_string("Original graph scores", scores)

#     update_print()
#     G_enemies_cut = remove_small_components(G_enemies)
#     scores = _run_analysis(G_enemies_cut, colors_countries, colors_regions, f"{output_dir}enemies_cut/")
#     analysis_str += _pretty_string("Cut graph scores", scores)

#     # Complete
#     analysis_str += "All commanders\n"

#     update_print()
#     G_all = nx.Graph()
#     G_all.add_edges_from(allies)
#     G_all.add_edges_from(enemies)
#     scores = _run_analysis(G_all, colors_countries, colors_regions, f"{output_dir}all_full/")
#     analysis_str += _pretty_string("Original graph scores", scores)

#     update_print()
#     G_all_cut = remove_small_components(G_all)
#     scores = _run_analysis(G_all_cut, colors_countries, colors_regions, f"{output_dir}all_cut/")
#     analysis_str += _pretty_string("Cut graph scores", scores)

#     print()

#     os.makedirs(os.path.dirname(analysis_file_path), exist_ok=True)
#     with open(analysis_file_path, "w", encoding="utf-8") as f:
#         f.write(analysis_str)


def _run_analysis(G: nx.Graph, colors_countries: dict, 
                  colors_regions: dict, output_path: str) -> dict[str, dict[str, dict[str, float]]]:
    pos = nx.spring_layout(G, seed=42)
    scores = {}

    scores['countries'] = run_predictions(G, colors_countries, pos, f"{output_path}countries_pred_")
    save_graph_as_img(G, colors_countries, f"{output_path}countries.png", pos=pos)

    scores['regions'] = run_predictions(G, colors_regions, pos, f"{output_path}regions_pred_")
    save_graph_as_img(G, colors_regions, f"{output_path}regions.png", pos=pos)

    return scores

def run_predictions(G: nx.Graph, colors: dict, pos: dict, output_path: str) -> tuple[dict[str, dict[str, float]], dict[str, dict]]:
    n_communities = len(set(colors.values()))

    scores = {}

    random_guessed = [set() for _ in range(n_communities)]
    for node in G.nodes:
        random_guessed[random.randint(0, n_communities - 1)].add(node)
    random_colors = colors_from_sets(random_guessed)
    # save_graph_as_img(G, random_colors, f"{output_path}_random.png", pos=pos)
    scores['random'] = _evaluate_prediction(G, colors, random_guessed)

    greedy_guessed = nx.community.greedy_modularity_communities(G)
    greedy_colors = colors_from_sets(greedy_guessed)
    # save_graph_as_img(G, greedy_colors, f"{output_path}_greedy.png", pos=pos)
    scores['greedy'] = _evaluate_prediction(G, colors, greedy_guessed)

    louvain_guessed = nx.community.louvain_communities(G, seed=42)
    louvain_colors = colors_from_sets(louvain_guessed)
    # save_graph_as_img(G, louvain_colors, f"{output_path}_louvain.png", pos=pos)
    scores['louvain'] = _evaluate_prediction(G, colors, louvain_guessed)

    label_prop_guessed = nx.community.label_propagation_communities(G)
    label_prop_colors = colors_from_sets(label_prop_guessed)
    # save_graph_as_img(G, label_prop_colors, f"{output_path}_label_prop.png", pos=pos)
    scores['label_prop'] = _evaluate_prediction(G, colors, label_prop_guessed)

    _colors = {
        "random": random_colors,
        "greedy": greedy_colors,
        "louvain": louvain_colors,
        "label_prop": label_prop_colors
    }

    return scores, _colors

def _evaluate_prediction(G: nx.Graph, colors: dict, guessed_communities: list) -> dict[str, float]:
    target = { com: colors[com] for com in G.nodes if com in colors }
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

def _pretty_string(section: str, scores: dict[str, dict[str, dict[str, float]]]) -> str:
    res = f"{section}:\n"
    for graph_type, preds in scores.items():
        res += f"{graph_type}:\n"
        for pred_type, metrics in preds.items():
            for metric, score in metrics.items():
                res += f"\t{pred_type} - {metric}: {score:.4f}\n"
    return res


def _pretty_print(section: str, scores: dict[str, dict[str, dict[str, float]]]):
    print(_pretty_string(section, scores))








if __name__ == "__main__":
    # predict_communities()
    pass