"""
Treemap
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.synthes.netw.co_occur.treemap_1.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.netw.co_occur.treemap_2.html"
    height="800px" width="100%" frameBorder="0"></iframe>

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy, AssociationIndex
    >>> from tm2p.synthes.netw.co_occur import Treemap
    >>> fig = (
    ...     Treemap()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # PLOT:
    ...     .using_title_text(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.co_occur.treemap_1.html")

    >>> fig = (
    ...     Treemap()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # NETWORK:
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # PLOT:
    ...     .using_title_text(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.netw.co_occur.treemap_2.html")

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_node_colors_based_on_group_attribute,
    cluster_nx_graph,
    plot_node_treemap,
)
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class Treemap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        nx_graph = assign_node_colors_based_on_group_attribute(nx_graph)
        return plot_node_treemap(self.params, nx_graph)
