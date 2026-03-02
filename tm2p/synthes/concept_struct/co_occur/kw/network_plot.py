"""
Network Plot
===============================================================================


Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.co_occurrence_network.keywords import NetworkPlot
    >>> plot = (
    ...     NetworkPlot()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     .using_association_index("association")
    ...     #
    ...     # PLOT:
    ...     .using_spring_layout_k(None)
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
    >>> plot.write_html("docsrc/_generated/px.packages.networks.co_occurrence.keywords.network_plot.html")

.. raw:: html

    <iframe src="../_generated/px.packages.networks.co_occurrence.keywords.network_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>



"""

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p.synthes.concept_struct.co_occur.usr.network_plot import (
    NetworkPlot as UserNetworkPlot,
)


class NetworkPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        return (
            UserNetworkPlot()
            .update(**self.params.__dict__)
            .with_source_field(Field.KW_NORM)
            .run()
        )
