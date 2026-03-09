"""
ItemsByCluster
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import ItemsByCluster
    >>> df = (
    ...     ItemsByCluster()
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
    >>> df
                                        0  ...                             2
    0                   fintech 117:25478  ...             banking 010:02599
    1       financial inclusion 017:03823  ...          innovation 009:01703
    2             green finance 011:02844  ...  financial services 007:01673
    3                blockchain 011:02023  ...          technology 007:01409
    4                     china 009:01947  ...
    5   artificial intelligence 008:01915  ...
    6              crowdfunding 007:01245  ...
    7                   regtech 006:01481  ...
    8            sustainability 006:01357  ...
    9           digital finance 005:02052  ...
    10                 covid-19 005:01068  ...
    11                    banks 005:00769  ...
    <BLANKLINE>
    [12 rows x 3 columns]


    >>> df = (
    ...     ItemsByCluster()
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
    >>> df  # doctest: +NORMALIZE_WHITESPACE
                              0                        1                   2
    0                   fintech     financial technology             banking
    1       financial inclusion       financial literacy          innovation
    2             green finance          economic growth  financial services
    3                blockchain  sustainable development          technology
    4                     china
    5   artificial intelligence
    6              crowdfunding
    7                   regtech
    8            sustainability
    9           digital finance
    10                 covid-19
    11                    banks


"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, extract_communities
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ItemsByCluster(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        communities = extract_communities(nx_graph)
        if use_counters is False:
            self.params.counters = False
            for col in communities.columns:
                communities[col] = communities[col].apply(remove_counters)
        return communities
