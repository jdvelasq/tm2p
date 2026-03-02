"""
Creates a co-occurrence networkx graph from a co-occurrence matrix.


"""

import networkx as nx  # type: ignore

from tm2p.discov.co_occur_matrix import Matrix as CoOccurrenceMatrix
from tm2p.discov.occur_matrix._normalize_matrix import _normalize_matrix


# -------------------------------------------------------------------------
def _step_01_create_co_occurrence_matrix(params):
    return (
        CoOccurrenceMatrix().update(**params.__dict__).update(term_counters=True).run()
    )


# -------------------------------------------------------------------------
def _step_02_normalize_matrix(params, matrix):
    return _normalize_matrix(params, matrix)


# -------------------------------------------------------------------------
def _step_03_add_nodes_to_nx_graph_from(
    nx_graph,
    cooc_matrix,
):
    matrix = cooc_matrix.copy()
    nodes = matrix.columns.tolist()
    nx_graph.add_nodes_from(nodes, group=0)

    for node in nx_graph.nodes():
        #
        # Remove metrics from the text property of the node name
        nx_graph.nodes[node]["text"] = " ".join(node.split(" ")[:-1])

    return nx_graph


# -------------------------------------------------------------------------
def _step_04_add_weighted_edges_to_nx_graph_from(
    nx_graph,
    cooc_matrix,
):
    matrix = cooc_matrix.copy()

    for i_row, row in enumerate(cooc_matrix.index.tolist()):
        for i_col, col in enumerate(cooc_matrix.columns.tolist()):
            #
            # Unicamente toma valores por encima de la diagonal principal
            if i_col <= i_row:
                continue

            weight = matrix.loc[row, col]
            if weight > 0:
                nx_graph.add_weighted_edges_from(
                    ebunch_to_add=[(row, col, weight)],
                    dash="solid",
                )

    return nx_graph


# -------------------------------------------------------------------------
def internal__create_nx_graph(params):

    nx_graph = nx.Graph()

    cooc_matrix = _step_01_create_co_occurrence_matrix(params)
    cooc_matrix = _step_02_normalize_matrix(params, cooc_matrix)
    nx_graph = _step_03_add_nodes_to_nx_graph_from(nx_graph, cooc_matrix)
    nx_graph = _step_04_add_weighted_edges_to_nx_graph_from(nx_graph, cooc_matrix)

    return nx_graph
