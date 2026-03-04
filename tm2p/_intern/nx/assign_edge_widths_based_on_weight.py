import numpy as np


def assign_edge_widths_based_on_weight(
    params,
    nx_graph,
):
    edge_width_range = params.edge_width_range

    #
    widths = np.array([nx_graph.edges[edge]["weight"] for edge in nx_graph.edges()])

    #
    # Sets the lower value to edge_width_min
    min_width = min(widths)
    widths = widths - min_width + edge_width_range[0]

    #
    # Checks if widths.max() > edge_width_max and, if so, rescales
    if widths.max() > edge_width_range[1]:
        #
        # Scales the edge width to the range [edge_width_min, edge_width_max]
        widths -= edge_width_range[0]
        widths /= widths.max() - edge_width_range[0]
        widths *= edge_width_range[1] - edge_width_range[0]
        widths += edge_width_range[0]

    #
    # Sets the value of edge_width
    for width, edge in zip(widths, nx_graph.edges()):
        nx_graph.edges[edge]["width"] = width

    return nx_graph
