"""
Network Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_authors import NetworkPlot
    >>> plot = (
    ...     NetworkPlot()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
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
    >>> plot.write_html("docsrc/_generated/px.packages.networks.co_citation.cited_authors.network_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.co_citation.cited_authors.network_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_cit._intern.network_plot import (
    NetworkPlot as InternalNetworkPlot,
)


class NetworkPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNetworkPlot()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_authors")
            .run()
        )
