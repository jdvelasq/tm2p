"""Node Degree Frame"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degree_dataframe,
)
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import internal__create_nx_graph


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = assign_degree_to_nodes(nx_graph)
        node_degrees = collect_node_degrees(nx_graph)
        data_frame = create_node_degree_dataframe(node_degrees)

        return data_frame
        node_degrees = collect_node_degrees(nx_graph)
        data_frame = create_node_degree_dataframe(node_degrees)

        return data_frame
