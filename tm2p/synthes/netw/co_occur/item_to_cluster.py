"""
ItemToCluster
===============================================================================


Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import ItemToCluster
    >>> mapping = (
    ...     ItemToCluster()
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
    ...     ItemToCluster()
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
    >>> from pprint import pprint
    >>> pprint(mapping)
    {'artificial intelligence': 0,
     'banking': 2,
     'banks': 0,
     'blockchain': 0,
     'china': 0,
     'covid-19': 0,
     'crowdfunding': 0,
     'digital finance': 0,
     'economic growth': 1,
     'financial inclusion': 0,
     'financial literacy': 1,
     'financial services': 2,
     'financial technology': 1,
     'fintech': 0,
     'green finance': 0,
     'innovation': 2,
     'regtech': 0,
     'sustainability': 0,
     'sustainable development': 1,
     'technology': 2}

"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import cluster_nx_graph, create_terms_to_clusters_mapping
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class ItemToCluster(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        mapping = create_terms_to_clusters_mapping(nx_graph)

        if use_counters is False:
            self.params.counters = False
            result = {}
            for key, value in mapping.items():
                result[remove_counters(key)] = value
            return result

        return mapping
