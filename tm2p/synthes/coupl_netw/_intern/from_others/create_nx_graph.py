import networkx as nx  # type: ignore
import numpy as np

from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.indic.bibliom_indic import BibliometricIndicators


# ------------------------------------------------------------------------------
def step_01_load_and_select_records(params):
    records = load_filtered_main_csv_zip(params=params)
    return records


# ------------------------------------------------------------------------------
def step_02_create_data_frame(params, records):

    unit_of_analysis = params.unit_of_analysis

    data_frame = records[[params.unit_of_analysis, "global_references"]]
    data_frame = data_frame.dropna()
    data_frame[unit_of_analysis] = (
        data_frame[unit_of_analysis]
        .str.split("; ")
        .map(lambda x: [y.strip() for y in x])
    )
    data_frame["global_references"] = (
        data_frame["global_references"]
        .str.split(";")
        .map(lambda x: [y.strip() for y in x])
    )

    data_frame = data_frame.explode(unit_of_analysis)
    data_frame = data_frame.explode("global_references")

    data_frame = data_frame.groupby(["global_references"], as_index=True).agg(
        {unit_of_analysis: list}
    )

    data_frame.columns = ["row"]
    data_frame["column"] = data_frame.row.copy()

    data_frame = data_frame.explode("row")
    data_frame = data_frame.explode("column")
    data_frame = data_frame.loc[data_frame.row != data_frame.column, :]
    data_frame = data_frame.groupby(["row", "column"], as_index=False).size()

    return data_frame


# ------------------------------------------------------------------------------
def step_03_filter_the_data_frame(params, data_frame):

    metrics = (
        BibliometricIndicators()
        .update(**params.__dict__)
        .with_source_field(params.unit_of_analysis)
        .run()
    )

    data_frame = data_frame.loc[data_frame.row.isin(metrics.index), :]
    data_frame = data_frame.loc[data_frame.column.isin(metrics.index), :]

    mapping = metrics["counters"].to_dict()

    data_frame["row"] = data_frame.row.map(mapping)
    data_frame["column"] = data_frame.column.map(mapping)

    data_frame.index = np.arange(len(data_frame))

    return data_frame


# ------------------------------------------------------------------------------
def step_04_adds_weighted_edges_to_nx_graph_from(data_frame, nx_graph):

    for _, row in data_frame.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row.row, row.column, row["size"])],
            dash="solid",
        )

    return nx_graph


# ------------------------------------------------------------------------------
def step_05_set_node_text_attribute(nx_graph):
    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = " ".join(node.split(" ")[:-1])
    return nx_graph


# ------------------------------------------------------------------------------
def internal__create_nx_graph(params):
    #
    # Create the networkx graph
    nx_graph = nx.Graph()

    records = step_01_load_and_select_records(params)
    data_frame = step_02_create_data_frame(params, records)
    data_frame = step_03_filter_the_data_frame(params, data_frame)
    nx_graph = step_04_adds_weighted_edges_to_nx_graph_from(data_frame, nx_graph)
    nx_graph = step_05_set_node_text_attribute(nx_graph)

    return nx_graph


# def __assign_group_from_dict(nx_graph, group_dict):
#     #
#     # The group is assigned using and external algorithm. It is designed
#     # to provide analysis capabilities to the system when other types of
#     # analysis are conducted, for example, factor analysis.
#     for node, group in group_dict.items():
#         nx_graph.nodes[node]["group"] = group
#     return nx_graph
#         nx_graph.nodes[node]["group"] = group
#     return nx_graph
