#
# In networkx, the size of the node is specified by the 'node_size' parameter.
# Example: nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
import numpy as np


def assign_textfont_sizes_based_on_citations(
    params,
    nx_graph,
):
    textfont_size_range = params.textfont_size_range

    #
    # Extracs occurrences from node names. Example: 'regtech 10:100' -> 10
    citations = list(nx_graph.nodes())
    citations = [node.split(" ")[-1] for node in citations]
    citations = [node.split(":")[1] for node in citations]
    citations = np.array([float(node) for node in citations])

    #
    # Set the lower value of the node size to node_size_min
    min_citations = min(citations)
    textfont_sizes = citations - min_citations + textfont_size_range[0]

    #
    # Checks if node_sizes.max() > node_size_max and, if so, rescales
    if textfont_sizes.max() > textfont_size_range[1]:
        #
        # Scales the node size to the range [node_size_min, node_size_max]
        textfont_sizes -= textfont_size_range[0]
        textfont_sizes /= textfont_sizes.max()
        textfont_sizes *= textfont_size_range[1] - textfont_size_range[0]
        textfont_sizes += textfont_size_range[0]

    #
    # Sets the value of node_size
    for size, node in zip(textfont_sizes, nx_graph.nodes()):
        nx_graph.nodes[node]["textfont_size"] = size

    return nx_graph
