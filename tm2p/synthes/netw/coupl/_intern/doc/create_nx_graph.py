import networkx as nx  # type: ignore
import numpy as np

from tm2p import Field
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits

GCS = Field.GCS.value
LCS = Field.LCS.value
YEAR = Field.YEAR.value
RID = Field.RID.value
LCR = Field.LCR_NORM.value
GCR = Field.GCR_WOS_FORMAT.value


# ------------------------------------------------------------------------------
def step_01_load_and_select_records(params):

    records = load_filtered_main_csv_zip(params=params)

    records = records.sort_values(
        [GCS, LCS, YEAR, RID],
        ascending=[False, False, False, True],
    )
    records = records.dropna(subset=[GCR])

    if params.citation_threshold is not None:
        records = records.loc[records[GCS] >= params.citation_threshold, :]
    if params.top_n is not None:
        records = records.head(params.top_n)

    return records


# ------------------------------------------------------------------------------
def step_02_adds_citations_to_record_id(params, records):

    _, gcs_digits = get_zero_digits(root_directory=params.root_directory)

    fmt = " 1:{:0" + str(gcs_digits) + "d}"
    records[RID] = records[RID] + records[GCS].map(fmt.format)
    return records


# ------------------------------------------------------------------------------
def step_03_create_citations_table(records):

    data_frame = records[[RID, GCR]]
    data_frame = data_frame.dropna()
    data_frame[RID] = (
        data_frame[RID].str.split("; ").map(lambda x: [y.strip() for y in x])
    )
    data_frame[GCR] = (
        data_frame[GCR].str.split(";").map(lambda x: [y.strip() for y in x])
    )

    data_frame = data_frame.explode(RID)
    data_frame = data_frame.explode(GCR)

    data_frame = data_frame.groupby([GCR], as_index=True).agg({RID: list})

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
        nx_graph.nodes[node]["text"] = node
    return nx_graph


# ------------------------------------------------------------------------------
def internal__create_nx_graph(params):

    nx_graph = nx.Graph()

    records = step_01_load_and_select_records(params)
    records = step_02_adds_citations_to_record_id(params, records)
    data_frame = step_03_create_citations_table(records)
    nx_graph = step_04_adds_weighted_edges_to_nx_graph_from(data_frame, nx_graph)
    nx_graph = step_05_set_node_text_attribute(nx_graph)

    return nx_graph
