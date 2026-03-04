import pandas as pd  # type: ignore

from tm2p._intern.nx.create_clusters_to_terms_mapping import (
    create_clusters_to_terms_mapping,
)
from tm2p.enum import Indicator


def summarize_communities(
    params,
    nx_graph,
):
    """Gets communities from a networkx graph as a data frame."""

    communities_dict = create_clusters_to_terms_mapping(
        params=params, nx_graph=nx_graph
    )
    communities_len = {}
    communities_perc = {}

    total = float(sum(len(communities_dict[key]) for key in communities_dict))

    for key, values in communities_dict.items():
        communities_len[key] = len(values)
        communities_perc[key] = round(communities_len[key] / total * 100, 1)
        communities_dict[key] = "; ".join(values)

    summary = pd.DataFrame(
        {
            Indicator.CLUSTER.value: list(communities_dict.keys()),
            Indicator.NUM_ITEMS.value: communities_len.values(),
            Indicator.PERCENTAGE.value: communities_perc.values(),
            Indicator.ITEMS.value: communities_dict.values(),
        }
    )

    summary = summary.sort_values(Indicator.CLUSTER.value, ascending=True)
    summary = summary.reset_index(drop=True)

    return summary
