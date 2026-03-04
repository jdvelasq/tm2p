def create_terms_to_clusters_mapping(
    nx_graph,
):
    """Creates a dictionary with terms as keys and clusters as values."""

    mapping = {}
    for node, data in nx_graph.nodes(data=True):
        cluster = data["group"]
        mapping[node] = cluster

    return mapping
