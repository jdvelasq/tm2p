"""
Node Degree Plot
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.organizations  import NodeDegreePlot
    >>> plot = (
    ...     NodeDegreePlot()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # PLOT:
    ...     .using_textfont_size(10)
    ...     .using_marker_size(7)
    ...     .using_line_color("black")
    ...     .using_line_width(1.5)
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
    >>> plot.write_html("docsrc/_generated/px.packages.networks.citation.organizations.network_degree_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.citation.organizations.network_degree_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>






"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.intellect_struct.cit_netw._intern.from_others.node_degree_plot import (
    NodeDegreePlot as OtherNodeDegreePlot,
)


class NodeDegreePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            OtherNodeDegreePlot()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("organizations")
            .run()
        )
