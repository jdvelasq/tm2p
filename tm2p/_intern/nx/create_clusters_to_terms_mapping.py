def create_clusters_to_terms_mapping(
    nx_graph,
):
    """Gets communities from a networkx graph as a dictionary."""

    # term_counters = params.term_counters

    mapping = {}

    for node, data in nx_graph.nodes(data=True):
        cluster = data["group"]
        if cluster not in mapping:
            mapping[cluster] = []
        mapping[cluster].append(node)

    return mapping
