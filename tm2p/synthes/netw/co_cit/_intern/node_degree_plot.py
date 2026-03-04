"""
Node Degree Plot
===============================================================================

## >>> from tm2p.packages.co_citation_network import NodeDegreePlot
## >>> plot = (
## ...     NodeDegreePlot()
## ...     .set_analysis_params(
## ...         unit_of_analysis="cited_sources", # "cited_sources",
## ...                                           # "cited_references",
## ...                                           # "cited_authors"
## ...     .having_items_in_top(30)
## ...     .using_citation_threshold(0)
## ...     .having_items_in(None)
## ...     #
## ...     # PLOT:
## ...     .using_line_color("black")
## ...     .using_line_width(1.5)
## ...     .using_marker_size(7)
## ...     .using_textfont_size(10)
## ...     .using_yshift(4)
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
## >>> plot.write_html("docsrc/__static/co_citation_network.node_degree_plot.html")

.. raw:: html

    <iframe src="../_static/co_citation_network.node_degree_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degree_dataframe,
    create_node_degree_plot,
)
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import internal__create_nx_graph


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
        data_frame = create_node_degree_dataframe(node_degrees)
        plot = create_node_degree_plot(self.params, data_frame)

        return plot
