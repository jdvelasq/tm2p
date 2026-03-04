"""
Network Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.documents import NetworkPlot
    >>> plot = (
    ...     NetworkPlot()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     .using_edge_colors(["#7793a5"])
    ...     .using_edge_width_range(0.8, 3.0)
    ...     .using_node_size_range(30, 70)
    ...     .using_textfont_opacity_range(0.35, 1.00)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     .using_xaxes_range(None, None)
    ...     .using_yaxes_range(None, None)
    ...     .using_axes_visible(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> plot.write_html("docsrc/_generated/px.packages.networks.citation.documents.network_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.citation.documents.network_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>





"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_constant_to_edge_colors,
    assign_edge_widths_based_on_weight,
    assign_node_colors_based_on_group_attribute,
    assign_node_sizes_based_on_citations,
    assign_text_positions_based_on_quadrants,
    assign_textfont_opacity_based_on_citations,
    assign_textfont_sizes_based_on_citations,
    cluster_nx_graph,
    compute_spring_layout_positions,
    plot_nx_graph,
)
from tm2p.synthes.netw.cit._intern.from_documents.create_nx_graph import (
    internal__create_nx_graph,
)


class NetworkPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        nx_graph = compute_spring_layout_positions(self.params, nx_graph)
        nx_graph = assign_node_colors_based_on_group_attribute(nx_graph)
        nx_graph = assign_node_sizes_based_on_citations(self.params, nx_graph)
        nx_graph = assign_textfont_sizes_based_on_citations(self.params, nx_graph)
        nx_graph = assign_textfont_opacity_based_on_citations(self.params, nx_graph)
        nx_graph = assign_edge_widths_based_on_weight(self.params, nx_graph)
        nx_graph = assign_text_positions_based_on_quadrants(nx_graph)
        nx_graph = assign_constant_to_edge_colors(self.params, nx_graph)

        return plot_nx_graph(self.params, nx_graph)
