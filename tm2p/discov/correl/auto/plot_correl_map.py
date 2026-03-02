import networkx as nx  # type: ignore

from tm2p._intern.nx import (
    internal__assign_node_sizes_based_on_occurrences,
    internal__assign_text_positions_based_on_quadrants,
    internal__assign_textfont_opacity_based_on_occurrences,
    internal__assign_textfont_sizes_based_on_occurrences,
    internal__compute_spring_layout_positions,
    internal__plot_nx_graph,
)


def add_nodes_from(params, nx_graph, data_frame):
    nodes = data_frame.columns.tolist()
    nx_graph.add_nodes_from(nodes, group=0, node_color=params.node_colors[0])
    return nx_graph


def assign_node_texts(nx_graph):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = node
    return nx_graph


def add_weighted_edges_from(
    params,
    nx_graph,
    data_frame,
):
    data_frame = data_frame.copy()

    # make values below lower diagonal equal to zero
    for i_col, col in enumerate(data_frame.columns):
        for i_row, row in enumerate(data_frame.index):
            if i_row >= i_col:
                data_frame.loc[row, col] = 0

    # Create a stacked matrix with the weights
    stacked_matrix = data_frame.stack().reset_index()
    stacked_matrix.columns = ["row", "col", "weight"]

    # Sort the stacked matrix by values, occurences, citations and names
    stacked_matrix["s_row"] = stacked_matrix["row"].apply(
        lambda x: x.split(" ")[-1] + " " + x.split(" ")[0]
    )
    stacked_matrix["s_col"] = stacked_matrix["col"].apply(
        lambda x: x.split(" ")[-1] + " " + x.split(" ")[0]
    )
    stacked_matrix = stacked_matrix.sort_values(
        by=["weight", "s_row", "s_col"],
        ascending=[False, False, False],
    )
    stacked_matrix = stacked_matrix.drop(columns=["s_row", "s_col"])

    # Filter similarity values
    stacked_matrix = stacked_matrix[stacked_matrix.weight > 0]
    stacked_matrix = stacked_matrix[
        stacked_matrix.weight >= params.edge_similarity_threshold
    ]

    # Extracts the top N values
    if params.edge_top_n is not None:
        stacked_matrix = stacked_matrix.head(params.edge_top_n)

    # Add the edges to the graph
    for _, row in stacked_matrix.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row["row"], row["col"], row["weight"])],
        )

    return nx_graph


def set_edge_properties(params, nx_graph):

    for edge in nx_graph.edges():

        weight = nx_graph.edges[edge]["weight"]

        if weight < 0.25:
            width, dash = params.edge_widths[0], "dot"
            edge_color = params.edge_colors[0]

        elif weight < 0.5:
            width, dash = params.edge_widths[1], "dash"
            edge_color = params.edge_colors[1]

        elif weight < 0.75:
            width, dash = params.edge_widths[2], "solid"
            edge_color = params.edge_colors[2]

        else:
            width, dash = params.edge_widths[3], "solid"
            edge_color = params.edge_colors[3]

        nx_graph.edges[edge]["width"] = width
        nx_graph.edges[edge]["dash"] = dash
        nx_graph.edges[edge]["color"] = edge_color

    return nx_graph


def plot_correl_map(
    params,
    data_frame,
):

    nx_graph = nx.Graph()

    nx_graph = add_nodes_from(params, nx_graph, data_frame)
    nx_graph = assign_node_texts(nx_graph)
    nx_graph = add_weighted_edges_from(params, nx_graph, data_frame)

    nx_graph = internal__compute_spring_layout_positions(params, nx_graph)
    nx_graph = internal__assign_node_sizes_based_on_occurrences(params, nx_graph)
    nx_graph = internal__assign_textfont_sizes_based_on_occurrences(params, nx_graph)
    nx_graph = internal__assign_textfont_opacity_based_on_occurrences(params, nx_graph)
    nx_graph = internal__assign_text_positions_based_on_quadrants(nx_graph)

    nx_graph = set_edge_properties(params, nx_graph)

    return internal__plot_nx_graph(params=params, nx_graph=nx_graph)
