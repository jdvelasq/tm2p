import networkx as nx  # type: ignore

from tm2p.discov.co_occur_matrix import Matrix as CoOccurrenceMatrix
from tm2p.synthes.netw.co_occur._intern.comput_assoc_index import comput_assoc_index


# -------------------------------------------------------------------------
def _create_co_occur_matrix(params):
    return CoOccurrenceMatrix().update(**params.__dict__).update(counters=True).run()


# -------------------------------------------------------------------------
def _normalize_co_occur_matrix(params, matrix):
    return comput_assoc_index(params.association_index, matrix)


# -------------------------------------------------------------------------
def _add_nodes_to_nx_graph_from(
    nx_graph,
    cooc_matrix,
):
    matrix = cooc_matrix.copy()
    nodes = matrix.columns.tolist()
    nx_graph.add_nodes_from(nodes, group=0)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["labeled"] = True
        nx_graph.nodes[node]["text"] = node

    return nx_graph


# -------------------------------------------------------------------------
def _add_weighted_edges_to_nx_graph_from(
    nx_graph,
    cooc_matrix,
):
    matrix = cooc_matrix.copy()

    for i_row, row in enumerate(cooc_matrix.index.tolist()):
        for i_col, col in enumerate(cooc_matrix.columns.tolist()):

            if i_col <= i_row:
                continue

            weight = matrix.loc[row, col]
            if weight > 0:
                nx_graph.add_weighted_edges_from(
                    ebunch_to_add=[(row, col, weight)],
                    dash="solid",
                )

    return nx_graph


def create_nx_graph(params):

    nx_graph = nx.Graph()

    co_occur_matrix = _create_co_occur_matrix(params)
    norm_co_occur_matrix = _normalize_co_occur_matrix(params, co_occur_matrix)
    nx_graph = _add_nodes_to_nx_graph_from(nx_graph, norm_co_occur_matrix)
    nx_graph = _add_weighted_edges_to_nx_graph_from(nx_graph, norm_co_occur_matrix)

    return nx_graph
