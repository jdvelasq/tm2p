def assign_constant_to_node_colors(
    params,
    nx_graph,
):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["node_color"] = params.node_colors[0]
    return nx_graph
