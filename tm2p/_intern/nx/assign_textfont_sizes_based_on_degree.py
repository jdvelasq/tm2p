#
# In networkx, the size of the node is specified by the 'node_size' parameter.
# Example: nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
import numpy as np


def assign_textfont_sizes_based_on_degree(
    params,
    nx_graph,
):
    textfont_size_range = params.textfont_size_range

    #
    # Compute node degree
    degrees = []
    for node in nx_graph.nodes():
        degrees.append(nx_graph.nodes[node]["degree"])
    degrees = np.array([float(degree) for degree in degrees])

    #
    # Set the lower value of the node size to node_size_min
    min_degree = min(degrees)
    textfont_sizes = degrees - min_degree + textfont_size_range[0]

    #
    # Checks if node_sizes.max() > node_size_max and, if so, rescales
    if textfont_sizes.max() > textfont_size_range[1]:
        #
        # Scales the node size to the range [node_size_min, node_size_max]
        textfont_sizes -= textfont_size_range[0]
        textfont_sizes /= textfont_sizes.max() - textfont_size_range[0]
        textfont_sizes *= textfont_size_range[1] - textfont_size_range[0]
        textfont_sizes += textfont_size_range[0]

    #
    # Sets the value of node_size
    for size, node in zip(textfont_sizes, nx_graph.nodes()):
        nx_graph.nodes[node]["textfont_size"] = size

    return nx_graph
