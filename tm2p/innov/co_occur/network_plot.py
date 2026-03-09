"""
Network Plot
===============================================================================


Smoke tests:
    >>> from tm2p.innov.co_occur import NetworkPlot
    >>> plot = (
    ...     NetworkPlot()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     .using_association_index("association")
    ...     .using_minimum_terms_in_cluster(5)
    ...     #
    ...     # PLOT:
    ...     .using_spring_layout_k(0.1)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     .using_node_size_range(30, 70)
    ...     .using_textfont_size_range(10, 20)
    ...     .using_textfont_opacity_range(0.35, 1.00)
    ...     .using_edge_colors(["#7793a5"])
    ...     .using_edge_width_range(0.8, 3.0)
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
    >>> plot.write_html("docsrc/_generated/px.experimental.co_occurrence.network_plot.html")

.. raw:: html

    <iframe src="../_generated/px.experimental.co_occurrence.network_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>



"""

from tm2p._intern import ParamsMixin
from tm2p.innov.co_occur.mixins import RecursiveClusteringMixin
from tm2p.synthes.netw.co_occur import NetworkPlot as ClassicalNetworkPlot


class NetworkPlot(
    ParamsMixin,
    RecursiveClusteringMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):
        pass

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:
            pass

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__build_final_network_plot(self):

        equivalence = {t.split(" ")[0]: t for t in self.terms_with_metrics}
        mapping = {}

        for i, terms in enumerate(self.discovered_clusters):
            for term in terms:
                key = equivalence[term]
                mapping[key] = i

        self.network_plot = (
            ClassicalNetworkPlot()
            .update(**self.params.__dict__)
            #
            .using_clustering_algorithm_or_dict(mapping)
            #
            .having_items_in_top(None)
            .having_items_ordered_by("OCC")
            .having_item_occurrences_between(None, None)
            .having_item_citations_between(None, None)
            .having_items_in(self.selected_terms)
            #
            .run()
        )

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self.internal__notify_process_start()
        self.internal__computer_recursive_clusters()
        self.internal__build_final_network_plot()
        self.internal__notify_process_end()

        return self.network_plot


#
