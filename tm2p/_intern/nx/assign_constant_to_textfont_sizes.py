def assign_constant_textfont_size_to_nodes(
    params,
    nx_graph,
):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["textfont_size"] = params.textfont_size
    return nx_graph
