import networkx as nx
import itertools

from comnet.visualizer.utils import get_edges_from_csv

def analyse_triads(output_file: str = "data/visualized/ww1/triads/analysis.txt"):
    allies = get_edges_from_csv("data/normalized/battles_allies.csv")
    enemies = get_edges_from_csv("data/normalized/battles_enemies.csv")
    
    G_allies = nx.Graph()
    G_allies.add_edges_from(allies)
    n_closed, n_open = count_triads(G_allies)
    _pretty_print_count("Allied", n_closed, n_open)

    G_enemies = nx.Graph()
    G_enemies.add_edges_from(enemies)
    n_closed, n_open = count_triads(G_enemies)
    _pretty_print_count("Opposed", n_closed, n_open)

    G_all = nx.Graph()
    G_all.add_edges_from(allies)
    G_all.add_edges_from(enemies)
    n_closed, n_open = count_triads(G_all)
    _pretty_print_count("All", n_closed, n_open)

    print(open_triad_types(allies, enemies))
    print(closed_triad_types(allies, enemies))

    _get_exceptions(allies, enemies)


def count_triads(G: nx.Graph) -> tuple[int, int]:
    _closed_count = _count_closed_triads(G)
    _open_count = _count_open_triads(G)
    return _closed_count, _open_count

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

def open_triad_types(edges_pos: set[tuple[str, str]], edges_neg: set[tuple[str, str]]):
    n_pos = {
        k: 0 for k in range(3)
    }
    G = nx.Graph()
    G.add_edges_from(edges_pos, pos=1, sign=1)
    G.add_edges_from(edges_neg, pos=0, sign=-1)

    exceptions = _get_exceptions(edges_pos, edges_neg)
    for u, v in exceptions:
        G[u][v].update(exc=True)

    for node in G.nodes:
        neighbors = G.neighbors(node)
        for n1, n2 in itertools.combinations(neighbors, 2):
            if G.has_edge(n1, n2):
                continue
            
            if 'exc' not in G[node][n1] and 'exc' not in G[node][n2]:
                n_pos[G[node][n1]['pos'] + G[node][n2]['pos']] += 1
                continue
            
            n1_opt = (G[node][n1]['pos'],) if 'exc' not in G[node][n1] else (0, 1)
            n2_opt = (G[node][n2]['pos'],) if 'exc' not in G[node][n2] else (0, 1)

            for n1_pos, n2_pos in itertools.product(n1_opt, n2_opt):
                n_pos[n1_pos + n2_pos] += 1

    return n_pos, exceptions
        

def closed_triad_types(edges_pos: set[tuple[str, str]], edges_neg: set[tuple[str, str]]):
    n_pos = {
        k: 0 for k in range(4)
    }
    G = nx.Graph()
    G.add_edges_from(edges_pos, pos=1, sign=1)
    G.add_edges_from(edges_neg, pos=0, sign=-1)
    
    exceptions = _get_exceptions(edges_pos, edges_neg)
    for u, v in exceptions:
        G[u][v].update(exc=True)

    for u, v, w in nx.all_triangles(G):
        if 'exc' not in G[u][v] and 'exc' not in G[v][w] and 'exc' not in G[w][u]:
            n_pos[G[u][v]['pos'] + G[v][w]['pos'] + G[w][u]['pos']] += 1
            continue
        
        uv_opt = (G[u][v]['pos'],) if 'exc' not in G[u][v] else (0, 1)
        vw_opt = (G[v][w]['pos'],) if 'exc' not in G[v][w] else (0, 1)
        wu_opt = (G[w][u]['pos'],) if 'exc' not in G[w][u] else (0, 1)

        for uv, vw, wu in itertools.product(uv_opt, vw_opt, wu_opt):
            n_pos[uv + vw + wu] += 1

    return n_pos, exceptions


def _get_exceptions(edges_pos: set[tuple[str, str]], edges_neg: set[tuple[str, str]]) -> list[tuple[str, str]]:
    sorted_p = sorted(sorted(edge) for edge in edges_pos)
    sorted_n = sorted(sorted(edge) for edge in edges_neg)

    exceptions = []
    for edge in sorted_p:
        if edge in sorted_n:
            exceptions.append(edge)
            
    return exceptions

def _pretty_print_count(title: str, n_closed: int, n_open: int):
    print(_pretty_string_count(title, n_closed, n_open))
    
def _pretty_string_count(title: str, n_closed: int, n_open: int) -> str:
    return f"{title}\nClosed triads: {n_closed}\nOpen triads: {n_open}\n"