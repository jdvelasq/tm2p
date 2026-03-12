import networkx as nx  # type: ignore
import numpy as np

from tm2p import Field
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits
from tm2p.anal.metrics.metrics import Metrics
from tm2p.enum import CouplingUnit

GCS = Field.GCS.value
LCS = Field.LCS.value
YEAR = Field.YEAR.value
RID = Field.RID.value
LCR = Field.LCR_NORM.value
GCR = Field.GCR_WOS_FORMAT.value


# ------------------------------------------------------------------------------
def step_01_load_and_select_records(params):
    records = load_filtered_main_csv_zip(params=params)
    return records


# ------------------------------------------------------------------------------
def step_02_create_data_frame(params, records):

    unit_of_analysis = params.coupling_unit.value

    df = records[[unit_of_analysis, GCR]]
    df = df.dropna()
    df[unit_of_analysis] = (
        df[unit_of_analysis].str.split("; ").map(lambda x: [y.strip() for y in x])
    )
    df[GCR] = df[GCR].str.split(";").map(lambda x: [y.strip() for y in x])

    df = df.explode(unit_of_analysis)
    df = df.explode(GCR)

    df = df.groupby([GCR], as_index=True).agg({unit_of_analysis: list})

    df.columns = ["row"]
    df["column"] = df.row.copy()

    df = df.explode("row")
    df = df.explode("column")
    df = df.loc[df.row != df.column, :]
    df = df.groupby(["row", "column"], as_index=False).size()

    return df


# ------------------------------------------------------------------------------
def step_03_filter_the_data_frame(params, data_frame):

    if params.coupling_unit == CouplingUnit.AUTH:
        source_field = Field.AUTH_NORM
    elif params.coupling_unit == CouplingUnit.CTRY:
        source_field = Field.CTRY_ISO3
    elif params.coupling_unit == CouplingUnit.ORG:
        source_field = Field.ORG
    elif params.coupling_unit == CouplingUnit.SRC:
        source_field = Field.SRC_ISO4_NORM
    else:
        raise ValueError("Invalid coupling unit")

    metrics = Metrics().update(**params.__dict__).with_source_field(source_field).run()

    data_frame = data_frame.loc[data_frame.row.isin(metrics.index), :]
    data_frame = data_frame.loc[data_frame.column.isin(metrics.index), :]

    mapping = metrics["COUNTERS"].to_dict()

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
        nx_graph.nodes[node]["text"] = node
    return nx_graph


# ------------------------------------------------------------------------------
def create_nx_graph(params):
    #
    # Create the networkx graph
    nx_graph = nx.Graph()

    records = step_01_load_and_select_records(params)
    data_frame = step_02_create_data_frame(params, records)
    data_frame = step_03_filter_the_data_frame(params, data_frame)
    nx_graph = step_04_adds_weighted_edges_to_nx_graph_from(data_frame, nx_graph)
    nx_graph = step_05_set_node_text_attribute(nx_graph)

    return nx_graph
