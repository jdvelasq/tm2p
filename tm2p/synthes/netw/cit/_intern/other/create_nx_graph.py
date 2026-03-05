import networkx as nx  # type: ignore

from tm2p import CitationUnit, Field, Indicator
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits
from tm2p.anal.metrics import Metrics

GCS = Field.GCS.value
LCS = Field.LCS.value
YEAR = Field.YEAR.value
RID = Field.RID.value
LCR = Field.LCR_NORM.value
CITING_UNIT = "CITING_UNIT"
CITED_UNIT = "CITED_UNIT"
OCC = Indicator.OCC.value


def create_nx_graph(params):
    #
    # Create the networkx graph
    nx_graph = nx.Graph()

    nx_graph = _add_weighted_edges_from(params=params, nx_graph=nx_graph)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = node

    return nx_graph


def _add_weighted_edges_from(
    params,
    nx_graph,
):
    citation_unit = params.citation_unit.value

    records = load_filtered_main_csv_zip(params)

    #
    # data_frame contains the citing and cited articles.
    data_frame = records[[RID, LCR]].copy()
    data_frame = data_frame.dropna()
    data_frame[LCR] = data_frame[LCR].str.split(";")
    data_frame = data_frame.explode(LCR)  # type: ignore
    data_frame[LCR] = data_frame[LCR].str.strip()
    data_frame.columns = [CITING_UNIT, CITED_UNIT]  # type: ignore

    records.index = records[RID].copy()

    article2unit = {
        row[RID]: row[citation_unit]
        for _, row in records[[RID, citation_unit]].iterrows()
    }
    data_frame[CITING_UNIT] = data_frame[CITING_UNIT].map(article2unit)
    data_frame[CITED_UNIT] = data_frame[CITED_UNIT].map(article2unit)

    #
    # Explode columns to find the relationships
    data_frame[CITING_UNIT] = data_frame[CITING_UNIT].str.split(";")
    data_frame = data_frame.explode(CITING_UNIT)  # type: ignore
    data_frame[CITING_UNIT] = data_frame[CITING_UNIT].str.strip()

    data_frame[CITED_UNIT] = data_frame[CITED_UNIT].str.split(";")
    data_frame = data_frame.explode(CITED_UNIT)  # type: ignore
    data_frame[CITED_UNIT] = data_frame[CITED_UNIT].str.strip()

    #
    # Compute citations and occurrences
    if params.citation_unit == CitationUnit.AUTH:
        source_field = Field.AUTH_NORM
    elif params.citation_unit == CitationUnit.CTRY:
        source_field = Field.CTRY_ISO3
    elif params.citation_unit == CitationUnit.ORG:
        source_field = Field.ORG
    elif params.citation_unit == CitationUnit.SRC:
        source_field = Field.SRC_ISO4_NORM
    else:
        raise ValueError("Invalid citation unit")

    metrics = Metrics().update(**params.__dict__).with_source_field(source_field).run()

    data_frame = data_frame.loc[
        data_frame[CITING_UNIT].isin(metrics.index.to_list()), :
    ]
    data_frame = data_frame.loc[data_frame[CITED_UNIT].isin(metrics.index.to_list()), :]

    #
    # Adds citations and occurrences to items
    occ_digits, gcs_digits = get_zero_digits(root_directory=params.root_directory)

    fmt_occ = "{:0" + str(occ_digits) + "d}"
    fmt_citations = "{:0" + str(gcs_digits) + "d}"

    rename_dict = {
        key: value
        for key, value in zip(
            metrics.index.to_list(),
            (
                metrics.index
                + " "
                + metrics[OCC].map(fmt_occ.format)
                + ":"
                + metrics[GCS].map(fmt_citations.format)
            ).to_list(),
        )
    }

    data_frame[CITING_UNIT] = data_frame[CITING_UNIT].map(rename_dict)
    data_frame[CITED_UNIT] = data_frame[CITED_UNIT].map(rename_dict)

    #
    # Computes the number of citations per citing_unit-cited_unit pair
    data_frame = data_frame.groupby(
        [CITING_UNIT, CITED_UNIT],
        as_index=False,
    ).size()

    #
    # Adds the data to the network:
    for _, row in data_frame.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row[CITING_UNIT], row[CITED_UNIT], row["size"])],
            dash="solid",
        )

    return nx_graph


# def __assign_group_from_dict(nx_graph, group_dict):
#     #
#     # The group is assigned using and external algorithm. It is designed
#     # to provide analysis capabilities to the system when other types of
#     # analysis are conducted, for example, factor analysis.
#     for node, group in group_dict.items():
#         nx_graph.nodes[node]["group"] = group
#     return nx_graph
