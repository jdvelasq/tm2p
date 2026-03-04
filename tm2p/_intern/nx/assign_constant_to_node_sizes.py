def assign_constant_to_node_sizes(
    params,
    nx_graph,
):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["node_size"] = params.node_size
    return nx_graph
