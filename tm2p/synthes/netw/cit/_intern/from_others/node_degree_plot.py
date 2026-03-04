from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degree_dataframe,
    create_node_degree_plot,
)
from tm2p._intern.nx.assign_degree_to_nodes import assign_degree_to_nodes
from tm2p.synthes.netw.cit._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class NodeDegreePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = assign_degree_to_nodes(nx_graph)
        node_degrees = collect_node_degrees(nx_graph)
        data_frame = create_node_degree_dataframe(node_degrees)
        plot = create_node_degree_plot(self.params, data_frame)

        return plot
