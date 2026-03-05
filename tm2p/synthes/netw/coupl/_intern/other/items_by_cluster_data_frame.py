from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, extract_communities
from tm2p.synthes.netw.coupl._intern.other.create_nx_graph import create_nx_graph


class ItemsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        communities = extract_communities(nx_graph)
        if use_counters is False:
            self.params.counters = False
            for col in communities.columns:
                communities[col] = communities[col].apply(remove_counters)
        return communities
