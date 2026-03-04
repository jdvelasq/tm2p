import networkx as nx  # type: ignore


def compute_circular_layout_positions(
    nx_graph,
):
    """Computes a circular layout with the last node as center"""

    pos = nx.circular_layout(nx_graph)
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["x"] = pos[node][0]
        nx_graph.nodes[node]["y"] = pos[node][1]

    return nx_graph
