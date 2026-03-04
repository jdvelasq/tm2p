#
# In networkx, the size of the node is specified by the 'node_size' parameter.
# Example: nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
import numpy as np


def assign_node_sizes_based_on_citations(
    params,
    nx_graph,
):
    #
    # Extracs occurrences from node names. Example: 'regtech 10:100' -> 10
    citations = list(nx_graph.nodes())
    citations = [node.split(" ")[-1] for node in citations]
    citations = [node.split(":")[1] for node in citations]
    citations = np.array([float(node) for node in citations])

    #
    # Set the lower value of the node size to node_size_min
    min_citations = min(citations)
    node_sizes = citations - min_citations + params.node_size_range[0]

    #
    # Checks if node_sizes.max() > node_size_max and, if so, rescales
    if node_sizes.max() > params.node_size_range[1]:
        #
        # Scales the node size to the range [node_size_min, node_size_max]
        node_sizes -= params.node_size_range[0]
        node_sizes /= node_sizes.max()
        node_sizes *= params.node_size_range[1]
        node_sizes += params.node_size_range[0]

    #
    # Sets the value of node_size
    for size, node in zip(node_sizes, nx_graph.nodes()):
        nx_graph.nodes[node]["node_size"] = size

    return nx_graph
