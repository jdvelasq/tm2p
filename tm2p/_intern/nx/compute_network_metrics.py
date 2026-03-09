import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

from tm2p.enum.column import (
    BETWEENNESS,
    CLOSENESS,
    CLUSTERING,
    CORE,
    DEGREE,
    EIGENVECTOR,
    PAGERANK,
    STRENGTH,
)


def compute_network_metrics(
    nx_graph,
):
    """Compute network statistics."""

    def compute_node_degree(nx_graph):
        """Computes the degree of each node in a networkx graph."""

        for node in nx_graph.nodes():
            nx_graph.nodes[node]["labeled"] = True

        return nx_graph

    nx_graph = compute_node_degree(nx_graph)

    nodes = list(nx_graph.nodes())
    occ_gc = [node.split(" ")[-1] for node in nodes]

    data_frame = pd.DataFrame(
        {
            DEGREE: nx.degree_centrality(nx_graph),
            BETWEENNESS: nx.betweenness_centrality(nx_graph),
            CLOSENESS: nx.closeness_centrality(nx_graph),
            PAGERANK: nx.pagerank(nx_graph),
            EIGENVECTOR: nx.eigenvector_centrality(nx_graph),
            CLUSTERING: nx.clustering(nx_graph),
            CORE: nx.core_number(nx_graph),
            STRENGTH: dict(nx_graph.degree(weight="weight")),
            "_occ_gc_": occ_gc,
            "_name_": nodes,
        },
        index=nodes,
    )

    data_frame = data_frame.sort_values(
        by=[DEGREE, "_occ_gc_", "_name_"],
        ascending=[False, False, True],
    )
    data_frame = data_frame.drop(columns=["_name_", "_occ_gc_"])

    return data_frame
