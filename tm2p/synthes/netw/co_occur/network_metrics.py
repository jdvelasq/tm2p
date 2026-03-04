"""
Metrics
===============================================================================

Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
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
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head(15)
                                       DEGREE  BETWEENNESS  CLOSENESS  PAGERANK
    fintech 117:25478                      19     0.268421   1.000000  0.268300
    financial inclusion 017:03823          13     0.075828   0.760000  0.068416
    financial technology 014:02508         11     0.050195   0.703704  0.048962
    banking 010:02599                      10     0.043275   0.678571  0.050895
    green finance 011:02844                 9     0.042788   0.655172  0.046914
    blockchain 011:02023                    9     0.023782   0.655172  0.050393
    technology 007:01409                    8     0.019688   0.633333  0.037425
    innovation 009:01703                    7     0.018519   0.612903  0.046957
    artificial intelligence 008:01915       7     0.011404   0.612903  0.039000
    financial services 007:01673            7     0.009942   0.612903  0.034420
    regtech 006:01481                       7     0.012671   0.612903  0.036532
    sustainable development 005:00604       7     0.015984   0.612903  0.031204
    digital finance 005:02052               6     0.007505   0.593750  0.030185
    covid-19 005:01068                      6     0.010721   0.593750  0.025856
    financial literacy 005:00665            6     0.006725   0.593750  0.027827




    >>> from tm2p.synthes.netw.co_occur import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
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
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head(15)


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import compute_network_metrics
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = create_nx_graph(self.params)
        return compute_network_metrics(params=self.params, nx_graph=nx_graph)
