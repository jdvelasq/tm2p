"""
Node Density Plot
===============================================================================


## >>> from tm2p.packages.co_citation_network import NodeDensityPlot
## >>> plot = (
## ...     NodeDensityPlot()
## ...     .set_analysis_params(
## ...         unit_of_analysis="cited_sources", # "cited_sources",
## ...                                           # "cited_references",
## ...                                           # "cited_authors"
## ...     .having_items_in_top(30)
## ...     .using_citation_threshold(0)
## ...     .having_items_in(None)
## ...     #
## ...     # CLUSTERING:
## ...     .using_clustering_algorithm_or_dict("louvain")
## ...     #
## ...     # NETWORK:
## ...     .using_spring_layout_k(None)
## ...     .using_spring_layout_iterations(30)
## ...     .using_spring_layout_seed(0)
## ...     #
## ...     # DENSITY:
## ...     .using_kernel_bandwidth(0.1)
## ...     .using_colormap("Aggrnyl")
## ...     .using_contour_opacity(0.6)
## ...     .using_textfont_size_range(10, 20)
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
## >>> plot.write_html("docsrc/__static/co_citation_network.node_density_plot.html")

.. raw:: html

    <iframe src="../_static/co_citation_network.node_density_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_textfont_sizes_based_on_occurrences,
    cluster_nx_graph,
    compute_spring_layout_positions,
    create_network_density_plot,
)
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import internal__create_nx_graph


class NodeDensityPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        nx_graph = compute_spring_layout_positions(self.params, nx_graph)
        nx_graph = assign_textfont_sizes_based_on_occurrences(self.params, nx_graph)

        return create_network_density_plot(self.params, nx_graph)
