def assign_degree_to_nodes(nx_graph):
    for node, adjacencies in nx_graph.adjacency():
        nx_graph.nodes[node]["degree"] = len(adjacencies)

    return nx_graph
