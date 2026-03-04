"""

## >>> from tm2p.coupling_network._core.others.node_density_plot import _node_density_plot
## >>> plot = _node_density_plot(
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
## ...     # DENSITY VISUALIZATION:
## ...     bandwidth=0.1,
## ...     colorscale="Aggrnyl",
## ...     opacity=0.6,
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
## >>> plot.write_html("docsrc/__static/coupling_network/_core/others.node_density_plot.html")

.. raw:: html

    <iframe src="../../_static/coupling_network/_core/others.node_density_plot.html"
    height="600px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_textfont_sizes_based_on_occurrences,
    cluster_nx_graph,
    compute_spring_layout_positions,
    create_network_density_plot,
)
from tm2p.synthes.netw.coupl._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class InternalNodeDensityPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(params=self.params)

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        nx_graph = compute_spring_layout_positions(self.params, nx_graph)
        nx_graph = assign_textfont_sizes_based_on_occurrences(self.params, nx_graph)

        return create_network_density_plot(self.params, nx_graph)
