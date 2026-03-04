"""
Terms by Cluster Data Frame
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import ItemsByClusterDataFrame
    >>> df = (
    ...     ItemsByClusterDataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
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

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import cluster_nx_graph, extract_communities_to_frame
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ItemsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        return extract_communities_to_frame(self.params, nx_graph)
