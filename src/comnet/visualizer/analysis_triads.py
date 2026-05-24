import networkx as nx
import itertools

from comnet.visualizer.utils import get_edges_from_csv

def analyse_triads(output_file: str = "data/visualized/ww1/triads/analysis.txt"):
    allies = get_edges_from_csv("data/normalized/battles_allies.csv")
    enemies = get_edges_from_csv("data/normalized/battles_enemies.csv")
    
    print("Allied")
    G_allies = nx.Graph()
    G_allies.add_edges_from(allies)
    count_triads(G_allies)

    print("Opposed")
    G_enemies = nx.Graph()
    G_enemies.add_edges_from(enemies)
    count_triads(G_enemies)

    print("All")
    G_all = nx.Graph()
    G_all.add_edges_from(allies)
    G_all.add_edges_from(enemies)
    count_triads(G_all)

    _correct_triads(allies, enemies)



def count_triads(G: nx.Graph):
    _closed_count = _count_closed_triads(G)
    _open_count = _count_open_triads(G)
    print(f"Closed: {_closed_count}\nOpen: {_open_count}, Ratio: {_closed_count / _open_count if _open_count > 0 else 'N/A'}")

def _count_open_triads(G: nx.Graph) -> int:
    count = 0
    for node in G.nodes:
        neighbors = G.neighbors(node)
        for n1, n2 in itertools.combinations(neighbors, 2):
            if not G.has_edge(n1, n2):
                count += 1
    return count    

def _count_closed_triads(G: nx.Graph) -> int:
    _dict = nx.triangles(G)
    assert isinstance(_dict, dict)
    return sum(_dict.values()) // 3

def _correct_triads(edges_pos: set[tuple[str, str]], edges_neg: set[tuple[str, str]]):
    n_pos = {
        k: 0 for k in range(4)
    }
    G = nx.Graph()
    G.add_edges_from(edges_pos, pos=1, sign=1)
    G.add_edges_from(edges_neg, pos=0, sign=-1)

    for u, v, w in nx.all_triangles(G):
        n_pos[G[u][v]['pos'] + G[v][w]['pos'] + G[w][u]['pos']] += 1
    
    for k in range(4):
        print(f"Triads with {k} positive edges: {n_pos[k]}")

    # print(f"Correct: {corr}, Incorrect: {incorr}, % correct: {corr / (corr + incorr) * 100 if (corr + incorr) > 0 else 'N/A'}")