import networkx as nx
from networkx.algorithms import community

def analyze_basic_stats(G: nx.Graph, com_to_country: dict[str, str]):
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()
    density = float(nx.density(G))
    communities = {country: set() for country in set(com_to_country.values())}
    for node in G.nodes():
        country = com_to_country.get(node, "Unknown")
        communities[country].add(node)

    modularity = community.modularity(G, communities.values())

    components = list(nx.connected_components(G))

    n_components = len(components)
    three_largest_components = list(len(c) for c in sorted(components, key=len, reverse=True)[:3])
    avg_component_size = sum(len(c) for c in components) / len(components) if components else 0
    std_component_size = (sum((len(c) - avg_component_size) ** 2 for c in components) / len(components)) ** 0.5 if components else 0
    median_component_size = sorted(len(c) for c in components)[len(components) // 2] if components else 0

    countries_dict = {}
    for node in G.nodes():
        country = com_to_country.get(node, "Unknown")
        if country not in countries_dict:
            countries_dict[country] = 0
        countries_dict[country] += 1

    n_countries = len(countries_dict)
    three_largest_countries = list((c, size) for c, size in sorted(countries_dict.items(), key=lambda x: x[1], reverse=True)[:3])
    avg_country_size = sum(countries_dict.values()) / len(countries_dict) if countries_dict else 0
    median_country_size = sorted(countries_dict.values())[len(countries_dict) // 2] if countries_dict else 0
    std_country_size = (sum((size - avg_country_size) ** 2 for size in countries_dict.values()) / len(countries_dict)) ** 0.5 if countries_dict else 0

    return {
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        "density": density,
        "modularity": modularity,
        "n_components": n_components,
        "three_largest_components": three_largest_components,
        "avg_component_size": avg_component_size,
        "median_component_size": median_component_size,
        "std_component_size": std_component_size,
        "n_countries": n_countries,
        "three_largest_countries": three_largest_countries,
        "avg_country_size": avg_country_size,
        "median_country_size": median_country_size,
        "std_country_size": std_country_size
    }