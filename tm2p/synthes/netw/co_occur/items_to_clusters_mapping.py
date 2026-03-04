"""
Terms to Cluster Mapping
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import ItemsToClustersMapping
    >>> mapping = (
    ...     ItemsToClustersMapping()
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
    {'artificial intelligence 008:01915': 0,
     'banking 010:02599': 2,
     'banks 005:00769': 0,
     'blockchain 011:02023': 0,
     'china 009:01947': 0,
     'covid-19 005:01068': 0,
     'crowdfunding 007:01245': 0,
     'digital finance 005:02052': 0,
     'economic growth 005:00660': 1,
     'financial inclusion 017:03823': 0,
     'financial literacy 005:00665': 1,
     'financial services 007:01673': 2,
     'financial technology 014:02508': 1,
     'fintech 117:25478': 0,
     'green finance 011:02844': 0,
     'innovation 009:01703': 2,
     'regtech 006:01481': 0,
     'sustainability 006:01357': 0,
     'sustainable development 005:00604': 1,
     'technology 007:01409': 2}


    >>> mapping = (
    ...     ItemsToClustersMapping()
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
    ...     .using_item_counters(False)
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
    >>> from pprint import pprint
    >>> pprint(mapping)



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    internal__cluster_nx_graph,
    internal__create_terms_to_clusters_mapping,
)
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ItemsToClustersMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = create_nx_graph(self.params)
        nx_graph = internal__cluster_nx_graph(self.params, nx_graph)
        return internal__create_terms_to_clusters_mapping(self.params, nx_graph)
