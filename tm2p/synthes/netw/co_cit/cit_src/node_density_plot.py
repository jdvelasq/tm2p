"""
Node Density Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_sources import NodeDensityPlot
    >>> plot = (
    ...     NodeDensityPlot()
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
    ...     # DENSITY:
    ...     .using_kernel_bandwidth(0.1)
    ...     .using_colormap("Aggrnyl")
    ...     .using_contour_opacity(0.6)
    ...     .using_textfont_size_range(10, 20)
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
    >>> plot.write_html("docsrc/_generated/px.packages.networks.co_citation.cited_sources.node_density_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.co_citation.cited_sources.node_density_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_cit._intern.node_density_plot import (
    NodeDensityPlot as InternalNodeDensityPlot,
)


class NodeDensityPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNodeDensityPlot()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_sources")
            .run()
        )
