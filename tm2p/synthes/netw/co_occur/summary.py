"""
Summary
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import Summary
    >>> df = (
    ...     Summary()
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
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(10)
       CLUSTER  ...                                              ITEMS
    0        0  ...  fintech 117:25478; financial inclusion 017:038...
    1        1  ...  financial technology 014:02508; financial lite...
    2        2  ...  banking 010:02599; innovation 009:01703; finan...
    <BLANKLINE>
    [3 rows x 4 columns]


    >>> df = (
    ...     Summary()
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
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(10)
       CLUSTER  ...                                              ITEMS
    0        0  ...  fintech; financial inclusion; green finance; b...
    1        1  ...  financial technology; financial literacy; econ...
    2        2  ...  banking; innovation; financial services; techn...
    <BLANKLINE>
    [3 rows x 4 columns]


"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, summarize_communities
from tm2p.enum.column import ITEMS
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class Summary(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        df = summarize_communities(self.params, nx_graph)
        if use_counters is False:
            self.params.counters = False
            df[ITEMS] = df[ITEMS].apply(
                lambda x: "; ".join([remove_counters(item) for item in x.split("; ")])
            )
        self.params.counters = use_counters

        return df
