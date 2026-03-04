from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    internal__assign_textfont_sizes_based_on_occurrences,
    internal__cluster_nx_graph,
    internal__compute_spring_layout_positions,
    internal__create_network_density_plot,
)
from tm2p.synthes.netw.cit._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class NodeDensityPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = internal__cluster_nx_graph(self.params, nx_graph)
        nx_graph = internal__compute_spring_layout_positions(self.params, nx_graph)
        nx_graph = internal__assign_textfont_sizes_based_on_occurrences(
            self.params, nx_graph
        )

        return internal__create_network_density_plot(self.params, nx_graph)
