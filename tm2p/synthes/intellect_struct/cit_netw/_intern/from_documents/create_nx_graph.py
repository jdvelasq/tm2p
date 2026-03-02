import networkx as nx  # type: ignore
import numpy as np

from tm2p._intern.data_access import load_filtered_main_csv_zip


# -------------------------------------------------------------------------
def _step_01_load_records(params):
    return load_filtered_main_csv_zip(params=params)


# -------------------------------------------------------------------------
def _step_02_sort_and_filter_records(params, records):

    records = records.sort_values(
        ["global_citations", "local_citations", "year", "record_id"],
        ascending=[False, False, False, True],
    )

    # Note: Same order of selection of VOSviewer
    if params.citation_threshold is not None:
        records = records.loc[records.global_citations >= params.citation_threshold, :]
    if params.top_n is not None:
        records = records.head(params.top_n)

    #
    # data_frame contains the citing and cited articles.
    records = records[["record_id", "local_references", "global_citations"]]

    return records


# -------------------------------------------------------------------------
def _step_03_explode_local_references(data_frame):
    data_frame.loc[:, "local_references"] = data_frame.local_references.str.split(";")
    data_frame = data_frame.explode("local_references")
    data_frame["local_references"] = data_frame["local_references"].str.strip()
    return data_frame


# -------------------------------------------------------------------------
def _step_04_get_dataframe_with_links(data_frame):
    # Local references must be in article column
    data_frame_with_links = data_frame[
        data_frame["local_references"].map(
            lambda x: x in data_frame.record_id.to_list()
        )
    ]
    return data_frame_with_links


# -------------------------------------------------------------------------
def _step_05_adds_citations_to_the_article(records, data_frame, data_frame_with_links):

    max_citations = records.global_citations.max()

    n_zeros_citations = int(np.log10(max_citations - 1)) + 1
    fmt = " 1:{:0" + str(n_zeros_citations) + "d}"
    #
    rename_dict = {
        key: value
        for key, value in zip(
            data_frame["record_id"].to_list(),
            (
                data_frame["record_id"] + data_frame["global_citations"].map(fmt.format)
            ).to_list(),
        )
    }
    #
    data_frame_with_links.loc[:, "record_id"] = data_frame_with_links["record_id"].map(
        rename_dict
    )
    data_frame_with_links.loc[:, "local_references"] = data_frame_with_links[
        "local_references"
    ].map(rename_dict)

    #
    # Removes documents without local citations in references
    data_frame = data_frame.dropna()

    return data_frame, data_frame_with_links


# -------------------------------------------------------------------------
def _step_06_adds_links_to_the_network(data_frame_with_links, nx_graph):
    # Adds the links to the network:
    for _, row in data_frame_with_links.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row.local_references, row.record_id, 1)],
            dash="solid",
        )

    return nx_graph


# -------------------------------------------------------------------------
def internal__create_nx_graph(params):

    records = _step_01_load_records(params)
    data_frame = _step_02_sort_and_filter_records(params, records)
    data_frame = _step_03_explode_local_references(data_frame)
    data_frame_with_links = _step_04_get_dataframe_with_links(data_frame)
    data_frame, data_frame_with_links = _step_05_adds_citations_to_the_article(
        records, data_frame, data_frame_with_links
    )

    nx_graph = nx.Graph()

    nx_graph = _step_06_adds_links_to_the_network(data_frame_with_links, nx_graph)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = " ".join(node.split(" ")[:-1])

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
