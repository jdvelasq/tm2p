"""
ClustersToItemsMapping
===============================================================================

Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import ClustersToItemsMapping
    >>> mapping = (
    ...     ClustersToItemsMapping()
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
    ...     .using_item_counters(True)
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
    >>> from pprint import pprint
    >>> pprint(mapping)
    {0: ['fintech 117:25478',
         'financial inclusion 017:03823',
         'green finance 011:02844',
         'blockchain 011:02023',
         'china 009:01947',
         'artificial intelligence 008:01915',
         'crowdfunding 007:01245',
         'regtech 006:01481',
         'sustainability 006:01357',
         'digital finance 005:02052',
         'covid-19 005:01068',
         'banks 005:00769'],
     1: ['financial technology 014:02508',
         'financial literacy 005:00665',
         'economic growth 005:00660',
         'sustainable development 005:00604'],
     2: ['banking 010:02599',
         'innovation 009:01703',
         'financial services 007:01673',
         'technology 007:01409']}



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    internal__cluster_nx_graph,
    internal__create_clusters_to_terms_mapping,
)
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ClustersToItemsMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = create_nx_graph(params=self.params)
        nx_graph = internal__cluster_nx_graph(params=self.params, nx_graph=nx_graph)
        mapping = internal__create_clusters_to_terms_mapping(
            params=self.params, nx_graph=nx_graph
        )

        return mapping
