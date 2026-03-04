import networkx as nx  # type: ignore


def compute_spring_layout_positions(
    params,
    nx_graph,
):
    """Computes the layout of a networkx graph."""

    pos = nx.spring_layout(
        nx_graph,
        k=params.spring_layout_k,
        iterations=params.spring_layout_iterations,
        seed=params.spring_layout_seed,
    )

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["x"] = pos[node][0]
        nx_graph.nodes[node]["y"] = pos[node][1]

    return nx_graph
