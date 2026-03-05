"""
Network Degree Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.synthes.netw.coupl.node_degree_plot_1.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.netw.coupl.node_degree_plot_2.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.netw.coupl.node_degree_plot_3.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.netw.coupl.node_degree_plot_4.html"
    height="800px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import CouplingUnit
    >>> from tm2p.synthes.netw.coupl import NodeDegreePlot
    >>> fig = (
    ...     NodeDegreePlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
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
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.coupl.node_degree_plot_1.html")


    >>> fig = (
    ...     NodeDegreePlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
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
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.coupl.node_degree_plot_2.html")




    >>> fig = (
    ...     NodeDegreePlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.SRC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
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
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.coupl.node_degree_plot_3.html")


    >>> fig = (
    ...     NodeDegreePlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.SRC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
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
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.coupl.node_degree_plot_4.html")


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import create_node_degree_plot

from .node_degree_dataframe import NodeDegreeDataFrame


class NodeDegreePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = NodeDegreeDataFrame().update(**self.params.__dict__).run()
        fig = create_node_degree_plot(self.params, df)

        return fig
