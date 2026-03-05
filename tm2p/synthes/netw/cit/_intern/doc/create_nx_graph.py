import networkx as nx  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits

GCS = Field.GCS.value
LCS = Field.LCS.value
YEAR = Field.YEAR.value
RID = Field.RID.value
LCR = Field.LCR_NORM.value


# -------------------------------------------------------------------------
def _step_02_sort_and_filter_records(params, records):

    records = records.sort_values(
        [GCS, LCS, YEAR, RID],
        ascending=[False, False, False, True],
    )

    if params.citation_threshold is not None:
        records = records.loc[records[GCS] >= params.citation_threshold, :]
    if params.top_n is not None:
        records = records.head(params.top_n)

    #
    # data_frame contains the citing and cited articles.
    records = records[[RID, LCR, GCS]]

    return records


# -------------------------------------------------------------------------
def _step_03_explode_local_references(data_frame):
    data_frame.loc[:, LCR] = data_frame[LCR].str.split("; ")
    data_frame = data_frame.explode(LCR)
    data_frame[LCR] = data_frame[LCR].str.strip()
    return data_frame


# -------------------------------------------------------------------------
def _step_04_get_dataframe_with_links(data_frame):
    # Local references must be in article column
    data_frame_with_links = data_frame[
        data_frame[LCR].map(lambda x: x in data_frame[RID].to_list())
    ]
    return data_frame_with_links


# -------------------------------------------------------------------------
def _step_05_adds_citations_to_the_article(
    params, records, data_frame, data_frame_with_links
):

    _, gcs_digits = get_zero_digits(root_directory=params.root_directory)

    fmt = " 1:{:0" + str(gcs_digits) + "d}"
    #
    rename_dict = {
        key: value
        for key, value in zip(
            data_frame[RID].to_list(),
            (data_frame[RID] + data_frame[GCS].map(fmt.format)).to_list(),
        )
    }
    #
    data_frame_with_links.loc[:, RID] = data_frame_with_links[RID].map(rename_dict)
    data_frame_with_links.loc[:, LCR] = data_frame_with_links[LCR].map(rename_dict)

    #
    # Removes documents without local citations in references
    data_frame = data_frame.dropna()

    return data_frame, data_frame_with_links


# -------------------------------------------------------------------------
def _step_06_adds_links_to_the_network(data_frame_with_links, nx_graph):
    # Adds the links to the network:
    for _, row in data_frame_with_links.iterrows():
        nx_graph.add_weighted_edges_from(
            ebunch_to_add=[(row[LCR], row[RID], 1)],
            dash="solid",
        )

    return nx_graph


# -------------------------------------------------------------------------
def create_nx_graph(params):

    records = load_filtered_main_csv_zip(params=params)

    df = _step_02_sort_and_filter_records(params, records)
    df = _step_03_explode_local_references(df)
    df_with_links = _step_04_get_dataframe_with_links(df)
    df, df_with_links = _step_05_adds_citations_to_the_article(
        params, records, df, df_with_links
    )

    nx_graph = nx.Graph()

    nx_graph = _step_06_adds_links_to_the_network(df_with_links, nx_graph)

    for node in nx_graph.nodes():
        nx_graph.nodes[node]["text"] = node

    return nx_graph
