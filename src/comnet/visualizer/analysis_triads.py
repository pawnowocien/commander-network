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





def count_triads(G: nx.Graph):
    print(f"Open: {_count_open_triads(G)}\nClosed: {_count_closed_triads(G)}")

def _count_open_triads(G: nx.Graph) -> int:
    count = 0
    for node in G.nodes:
        neighbors = G.neighbors(node)
        for n1, n2 in itertools.combinations(neighbors, 2):
            if not G.has_edge(n1, n2):
                count += 1
    return count    

def _count_closed_triads(G: nx.Graph) -> int:
    return sum(nx.triangles(G).values()) // 3