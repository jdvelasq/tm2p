import networkx as nx  # type: ignore
import numpy as np

from tm2p._intern.data_access import load_filtered_main_csv_zip


# ------------------------------------------------------------------------------
def step_01_load_and_select_records(params):

    records = load_filtered_main_csv_zip(params=params)

    records = records.sort_values(
        ["global_citations", "local_citations", "year", "record_id"],
        ascending=[False, False, False, True],
    )
    records = records.dropna(subset=["global_references"])

    if params.citation_threshold is not None:
        records = records.loc[records.global_citations >= params.citation_threshold, :]
    if params.top_n is not None:
        records = records.head(params.top_n)

    return records


# ------------------------------------------------------------------------------
def step_02_adds_citations_to_record_id(records):
    max_citations = records.global_citations.max()
    n_zeros_citations = int(np.log10(max_citations - 1)) + 1
    fmt = " 1:{:0" + str(n_zeros_citations) + "d}"
    records["record_id"] = records["record_id"] + records["global_citations"].map(
        fmt.format
    )
    return records


# ------------------------------------------------------------------------------
def step_03_create_citations_table(records):

    data_frame = records[["record_id", "global_references"]]
    data_frame = data_frame.dropna()
    data_frame["record_id"] = (
        data_frame["record_id"].str.split("; ").map(lambda x: [y.strip() for y in x])
    )
    data_frame["global_references"] = (
        data_frame["global_references"]
        .str.split(";")
        .map(lambda x: [y.strip() for y in x])
    )

    data_frame = data_frame.explode("record_id")
    data_frame = data_frame.explode("global_references")

    data_frame = data_frame.groupby(["global_references"], as_index=True).agg(
        {"record_id": list}
    )

    data_frame.columns = ["row"]
    data_frame["column"] = data_frame.row.copy()

    data_frame = data_frame.explode("row")
    data_frame = data_frame.explode("column")
    data_frame = data_frame.loc[data_frame.row != data_frame.column, :]
    data_frame = data_frame.groupby(["row", "column"], as_index=False).size()

    #
    # Formats only articles
    data_frame["row"] = (
        data_frame["row"]
        .str.split(", ")
        .map(lambda x: x[:2] + [x[2] + " " + x[-1].split(" ")[-1]])
        .str.join(", ")
    )
    #
    data_frame["column"] = (
        data_frame["column"]
        .str.split(", ")
        .map(lambda x: x[:2] + [x[2] + " " + x[-1].split(" ")[-1]])
        .str.join(", ")
    )

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

    nx_graph = nx.Graph()

    records = step_01_load_and_select_records(params)
    records = step_02_adds_citations_to_record_id(records)
    data_frame = step_03_create_citations_table(records)
    nx_graph = step_04_adds_weighted_edges_to_nx_graph_from(data_frame, nx_graph)
    nx_graph = step_05_set_node_text_attribute(nx_graph)

    return nx_graph


# ------------------------------------------------------------------------------
# def __assign_group_from_dict(nx_graph, group_dict):
#     #
#     # The group is assigned using and external algorithm. It is designed
#     # to provide analysis capabilities to the system when other types of
#     # analysis are conducted, for example, factor analysis.
#     for node, group in group_dict.items():
#         nx_graph.nodes[node]["group"] = group
#     return nx_graph
