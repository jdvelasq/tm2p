"""

## >>> from tm2p.coupling_network._core.others.network_plot import _network_plot
## >>> plot = _network_plot(
## ...     unit_of_analysis='authors', # authors, countries, organizations, sources
## ...     #
## ...     # COLUMN PARAMS:
## ...     top_n=20,
## ...     citations_threshold=0,
## ...     occurrence_threshold=2,
## ...     custom_terms=None,
## ...     #
## ...     # NETWORK PARAMS:
## ...     algorithm_or_dict="louvain",
## ...     ).set_nx_params(
## ...         nx_k=None,
## ...         nx_iterations=30,
## ...         nx_random_state=0,
## ...     #
## ...     # NODES:
## ...     node_size_range=(30, 70),
## ...     textfont_size_range=(10, 20),
## ...     textfont_opacity_range=(0.35, 1.00),
## ...     #
## ...     # EDGES:
## ...     edge_color="#7793a5",
## ...     edge_width_range=(0.8, 3.0),
## ...     ).set_axes_params(
## ...         xaxes_range=None,
## ...         yaxes_range=None,
## ...         show_axes=False,
## ...     #
## ...     # DATABASE:
## ...     .where_root_directory("tests/fintech/")
## ...     .where_database("main")
## ...     .where_record_years_range(None, None)
## ...     .where_record_citations_range(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .run()
## ... )
## >>> plot.write_html("docsrc/__static/coupling_network/_core/others.network_plot.html")

.. raw:: html

    <iframe src="../../_static/coupling_network/_core/others.network_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_constant_to_edge_colors,
    internal__assign_edge_widths_based_on_weight,
    internal__assign_node_colors_based_on_group_attribute,
    internal__assign_node_sizes_based_on_occurrences,
    internal__assign_text_positions_based_on_quadrants,
    internal__assign_textfont_opacity_based_on_occurrences,
    internal__assign_textfont_sizes_based_on_occurrences,
    internal__cluster_nx_graph,
    internal__compute_spring_layout_positions,
    internal__plot_nx_graph,
)
from tm2p.synthes.coupl_netw._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class InternalNetworkPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(params=self.params)

        nx_graph = internal__cluster_nx_graph(params=self.params, nx_graph=nx_graph)
        nx_graph = internal__compute_spring_layout_positions(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = internal__assign_node_colors_based_on_group_attribute(nx_graph)
        nx_graph = internal__assign_node_sizes_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = internal__assign_textfont_sizes_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = internal__assign_textfont_opacity_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = internal__assign_edge_widths_based_on_weight(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = internal__assign_text_positions_based_on_quadrants(nx_graph)
        nx_graph = assign_constant_to_edge_colors(params=self.params, nx_graph=nx_graph)

        return internal__plot_nx_graph(params=self.params, nx_graph=nx_graph)
