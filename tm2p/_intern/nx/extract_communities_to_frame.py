import pandas as pd  # type: ignore

from tm2p._intern import Params
from tm2p._intern.nx.create_clusters_to_terms_mapping import (
    internal__create_clusters_to_terms_mapping,
)


def internal__extract_communities_to_frame(
    params,
    nx_graph,
):
    """Gets communities from a networkx graph as a data frame."""

    def f(x):
        x = [(w.split(" ")[-1], w) for w in x]
        mapping = {}
        for w in x:
            if w[0] not in mapping:
                mapping[w[0]] = []
            mapping[w[0]].append(w[1])
        mapping = {k: sorted(v) for k, v in mapping.items()}
        x = [v for k in sorted(mapping.keys(), reverse=True) for v in mapping[k]]
        return x

    local_params = Params(**params.__dict__).update(item_counters=True)
    communities = internal__create_clusters_to_terms_mapping(local_params, nx_graph)
    communities = {key: f(value) for key, value in communities.items()}
    if params.item_counters is False:
        communities = {
            key: [" ".join(v.split(" ")[:-1]) for v in value]
            for key, value in communities.items()
        }
    communities = pd.DataFrame.from_dict(communities, orient="index").T
    communities = communities.fillna("")
    communities = communities.sort_index(axis=1)

    return communities
