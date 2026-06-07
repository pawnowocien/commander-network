import networkx as nx

def run_centrality_analysis(G: nx.Graph) -> dict[str, dict[str, float]]:
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    harmonic_centrality = nx.harmonic_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    return {
        "degree": degree_centrality,
        "closeness": closeness_centrality,
        "harmonic": harmonic_centrality,
        "betweenness": betweenness_centrality
    }
