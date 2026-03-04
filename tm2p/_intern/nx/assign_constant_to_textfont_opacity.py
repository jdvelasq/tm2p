def assign_constant_to_textfont_opacity(
    params,
    nx_graph,
):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["textfont_opacity"] = params.textfont_opacity
    return nx_graph
