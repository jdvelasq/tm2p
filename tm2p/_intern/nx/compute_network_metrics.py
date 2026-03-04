import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

from tm2p.enum import Indicator


def compute_network_metrics(
    nx_graph,
):
    """Compute network statistics."""

    def compute_node_degree(nx_graph):
        """Computes the degree of each node in a networkx graph."""

        for node, adjacencies in nx_graph.adjacency():
            nx_graph.nodes[node]["degree"] = len(adjacencies)
            nx_graph.nodes[node]["labeled"] = True

        return nx_graph

    nx_graph = compute_node_degree(nx_graph)

    nodes = list(nx_graph.nodes())
    degree = [nx_graph.nodes[node]["degree"] for node in nodes]

    occ_gc = [node.split(" ")[-1] for node in nodes]

    betweenness = nx.betweenness_centrality(nx_graph)
    closeness = nx.closeness_centrality(nx_graph)
    pagerank = nx.pagerank(nx_graph)

    #
    # Callon centrality - density map
    ## callon_matrix = nx_graph_to_co_occ_matrix(graph).astype(float)
    ## callon_centrality = callon_matrix.values.diagonal()
    ## callon_density = callon_matrix.sum() - callon_centrality
    ## strategic_diagram["callon_centrality"] *= 10
    ## strategic_diagram["callon_density"] *= 100

    data_frame = pd.DataFrame(
        {
            Indicator.DEGREE.value: degree,
            Indicator.BETWEENNESS.value: betweenness,
            Indicator.CLOSENESS.value: closeness,
            Indicator.PAGERANK.value: pagerank,
            # "Centrality": callon_centrality,
            # "Density": callon_density,
            # "_occ_": occ,
            # "_gc_": gc,
            "_occ_gc_": occ_gc,
            "_name_": nodes,
        },
        index=nodes,
    )

    data_frame = data_frame.sort_values(
        by=[Indicator.DEGREE.value, "_occ_gc_", "_name_"],
        ascending=[False, False, True],
    )
    data_frame = data_frame.drop(columns=["_name_", "_occ_gc_"])

    return data_frame
