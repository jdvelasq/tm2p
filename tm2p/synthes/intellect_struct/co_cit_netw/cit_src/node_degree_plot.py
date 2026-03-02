"""
Node Degree Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_sources import NodeDegreePlot
    >>> plot = (
    ...     NodeDegreePlot()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_line_color("black")
    ...     .using_line_width(1.5)
    ...     .using_marker_size(7)
    ...     .using_textfont_size(10)
    ...     .using_yshift(4)
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
    >>> plot.write_html("docsrc/_generated/px.packages.networks.co_citation.cited_sources.node_degree_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.co_citation.cited_sources.node_degree_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.intellect_struct.co_cit_netw._intern.node_degree_plot import (
    NodeDegreePlot as InternalNodeDegreePlot,
)


class NodeDegreePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNodeDegreePlot()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_sources")
            .run()
        )
