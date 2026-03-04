"""

## >>> from tm2p.coupling_network._core.others.node_degree_plot import _node_degree_plot
## >>> plot = _node_degree_plot(
## ...     unit_of_analysis='authors', # authors, countries, organizations, sources
## ...     #
## ...     # COLUMN PARAMS:
## ...     top_n=20,
## ...     citations_threshold=0,
## ...     occurrence_threshold=2,
## ...     custom_terms=None,
## ...     #
## ...     # DEGREE PLOT:
## ...     textfont_size=10,
## ...     marker_size=7,
## ...     line_color="black",
## ...     line_width=1.5,
## ...     yshift=4,
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
## >>> plot.write_html("docsrc/__static/coupling_network/_core/others.node_degree_plot.html")

.. raw:: html

    <iframe src="../../_static/coupling_network/_core/others.node_degree_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degree_dataframe,
    create_node_degree_plot,
)
from tm2p.synthes.netw.coupl._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class InternalNodeDegreePlot(
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
