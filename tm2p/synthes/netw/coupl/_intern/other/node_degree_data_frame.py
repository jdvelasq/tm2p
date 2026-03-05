from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degree_dataframe,
)
from tm2p.enum import Indicator
from tm2p.synthes.netw.coupl._intern.other.create_nx_graph import create_nx_graph


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(params=self.params)
        nx_graph = assign_degree_to_nodes(nx_graph)
        node_degrees = collect_node_degrees(nx_graph)
        df = create_node_degree_dataframe(node_degrees)

        if use_counters is False:
            self.params.counters = False
            df[Indicator.NAME.value] = (
                df[Indicator.NAME.value].str.split(" ").str[:-1].str.join(" ")
            )
        return df
