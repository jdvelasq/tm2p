"""
Creates a co-occurrence networkx graph from a co-occurrence matrix.


"""

from cdlib import algorithms  # type: ignore


def cluster_nx_graph(
    params,
    nx_graph,
):

    algorithm_or_dict = params.clustering_algorithm_or_dict

    if isinstance(algorithm_or_dict, str):
        nx_graph = _apply_cdlib_algorithm(nx_graph, algorithm_or_dict)

    if isinstance(algorithm_or_dict, dict):
        #
        # The group is assigned using and external algorithm. It is designed
        # to provide analysis capabilities to the system when other types of
        # analysis are conducted, for example, factor analysis.

        for node, group in algorithm_or_dict.items():
            nx_graph.nodes[node]["group"] = group

    for node in nx_graph.nodes:
        nx_graph.nodes[node]["top_n"] = False

    clusters = {}
    for node in nx_graph.nodes:
        group = nx_graph.nodes[node]["group"]
        if group not in clusters:
            clusters[group] = []
        clusters[group].append(node)

    for _, value in clusters.items():
        sorted_value = sorted(
            value,
            key=lambda x: int(x.split(" ")[-1].split(":")[0]),
            reverse=False,
        )
        for node in sorted_value[: params.node_n_labels]:
            nx_graph.nodes[node]["labeled"] = True

    return nx_graph


def _apply_cdlib_algorithm(
    nx_graph,
    algorithm,
):
    """Network community detection."""

    cdlib_algorithm = {
        "label_propagation": algorithms.label_propagation,
        "leiden": algorithms.leiden,
        "louvain": algorithms.louvain,
        "walktrap": algorithms.walktrap,
    }[algorithm]

    communities = []
    if algorithm == "label_propagation":
        communities = cdlib_algorithm(nx_graph).communities
    elif algorithm == "leiden":
        communities = cdlib_algorithm(nx_graph).communities
    elif algorithm == "louvain":
        communities = cdlib_algorithm(nx_graph, randomize=False).communities
    elif algorithm == "walktrap":
        communities = cdlib_algorithm(nx_graph).communities

    for i_community, community in enumerate(communities):
        for node in community:
            nx_graph.nodes[node]["group"] = i_community

    return nx_graph
