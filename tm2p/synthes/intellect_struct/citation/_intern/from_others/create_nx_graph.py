import networkx as nx  # type: ignore
import numpy as np

from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.anal._intern.performance.performance_metrics import (
    PerformanceMetrics as TermsByYearMetricsDataFrame,
)


def internal__create_nx_graph(params):
    #
    # Create the networkx graph
    nx_graph = nx.Graph()

    nx_graph = __add_weighted_edges_from(params=params, nx_graph=nx_graph)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = " ".join(node.split(" ")[:-1])

    return nx_graph


def __add_weighted_edges_from(
    params,
    nx_graph,
):
    unit_of_analysis = params.unit_of_analysis

    records = load_filtered_main_csv_zip(params)

    #
    # data_frame contains the citing and cited articles.
    data_frame = records[["record_id", "local_references"]]
    data_frame = data_frame.dropna()
    data_frame["local_references"] = data_frame.local_references.str.split(";")
    data_frame = data_frame.explode("local_references")
    data_frame["local_references"] = data_frame["local_references"].str.strip()
    data_frame.columns = ["citing_unit", "cited_unit"]

    records.index = records.record_id.copy()

    article2unit = {
        row.record_id: row[unit_of_analysis]
        for _, row in records[["record_id", unit_of_analysis]].iterrows()
    }
    data_frame["citing_unit"] = data_frame["citing_unit"].map(article2unit)
    data_frame["cited_unit"] = data_frame["cited_unit"].map(article2unit)

    #
    # Explode columns to find the relationships
    data_frame["citing_unit"] = data_frame["citing_unit"].str.split(";")
    data_frame = data_frame.explode("citing_unit")
    data_frame["citing_unit"] = data_frame["citing_unit"].str.strip()

    data_frame["cited_unit"] = data_frame["cited_unit"].str.split(";")
    data_frame = data_frame.explode("cited_unit")
    data_frame["cited_unit"] = data_frame["cited_unit"].str.strip()

    #
    # Compute citations and occurrences
    metrics = (
        TermsByYearMetricsDataFrame()
        .update(**params.__dict__)
        .with_source_field(params.unit_of_analysis)
        .run()
    )

    data_frame = data_frame.loc[data_frame.citing_unit.isin(metrics.index.to_list()), :]
    data_frame = data_frame.loc[data_frame.cited_unit.isin(metrics.index.to_list()), :]

    #
    # Adds citations and occurrences to items
    max_occ = metrics.OCC.max()
    n_zeros_occ = int(np.log10(max_occ - 1)) + 1
    fmt_occ = "{:0" + str(n_zeros_occ) + "d}"

    max_citations = metrics.global_citations.max()
    n_zeros_citations = int(np.log10(max_citations - 1)) + 1
    fmt_citations = "{:0" + str(n_zeros_citations) + "d}"

    rename_dict = {
        key: value
        for key, value in zip(
            metrics.index.to_list(),
            (
                metrics.index
                + " "
                + metrics["OCC"].map(fmt_occ.format)
                + ":"
                + metrics["global_citations"].map(fmt_citations.format)
            ).to_list(),
        )
    }

    data_frame["citing_unit"] = data_frame["citing_unit"].map(rename_dict)
    data_frame["cited_unit"] = data_frame["cited_unit"].map(rename_dict)

    #
    # Computes the number of citations per citing_unit-cited_unit pair
    data_frame = data_frame.groupby(
        ["citing_unit", "cited_unit"],
        as_index=False,
    ).size()

    #
    # Adds the data to the network:
    for _, row in data_frame.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row.citing_unit, row.cited_unit, row["size"])],
            dash="solid",
        )

    return nx_graph


def __assign_group_from_dict(nx_graph, group_dict):
    #
    # The group is assigned using and external algorithm. It is designed
    # to provide analysis capabilities to the system when other types of
    # analysis are conducted, for example, factor analysis.
    for node, group in group_dict.items():
        nx_graph.nodes[node]["group"] = group
    return nx_graph
