from tm2p._intern import ParamsMixin
from tm2p._intern.nx import compute_network_metrics
from tm2p.synthes.netw.coupl._intern.doc.create_nx_graph import (
    internal__create_nx_graph,
)


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(params=self.params)
        return compute_network_metrics(nx_graph=nx_graph)
