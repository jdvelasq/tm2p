"""
Metrics
===============================================================================

Smoke tests:
    >>> from tm2p import Field, AssociationIndex, ItemOrderBy
    >>> from tm2p.synthes.netw.co_occur import NetworkMetrics
    >>> df = (
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
    ...     .using_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())  # doctest: +NORMALIZE_WHITESPACE
                                      DEGREE  BETWEENNESS  CLOSENESS  PAGERANK  EIGENVECTOR  CLUSTERING  CORE  STRENGTH
    fintech 117:25478               1.000000     0.268421   1.000000  0.268300     0.426676    0.350877     5     109.0
    financial inclusion 017:03823   0.684211     0.075828   0.760000  0.068416     0.330603    0.448718     5      27.0
    financial technology 014:02508  0.578947     0.050195   0.703704  0.048962     0.283678    0.490909     5      18.0
    banking 010:02599               0.526316     0.043275   0.678571  0.050895     0.259523    0.466667     5      19.0
    green finance 011:02844         0.473684     0.042788   0.655172  0.046914     0.223218    0.444444     5      17.0



    >>> from tm2p.synthes.netw.co_occur import NetworkMetrics
    >>> df = (
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
    ...     .using_counters(False)
    ...     #
    ...     # NETWORK:
    ...     .using_association_index(AssociationIndex.NONE)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())  # doctest: +NORMALIZE_WHITESPACE
                            DEGREE  BETWEENNESS  CLOSENESS  PAGERANK  EIGENVECTOR  CLUSTERING  CORE  STRENGTH
    fintech               1.000000     0.268421   1.000000  0.268300     0.426676    0.350877     5     109.0
    financial inclusion   0.684211     0.075828   0.760000  0.068416     0.330603    0.448718     5      27.0
    financial technology  0.578947     0.050195   0.703704  0.048962     0.283678    0.490909     5      18.0
    banking               0.526316     0.043275   0.678571  0.050895     0.259523    0.466667     5      19.0
    green finance         0.473684     0.042788   0.655172  0.046914     0.223218    0.444444     5      17.0


"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import compute_network_metrics
from tm2p.synthes.netw.co_occur._intern.create_nx_graph import create_nx_graph


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        use_counters = self.params.counters
        self.params.counters = True
        nx_graph = create_nx_graph(self.params)
        df = compute_network_metrics(nx_graph=nx_graph)

        if use_counters is False:
            self.params.counters = False
            names = df.index.tolist()
            names = [remove_counters(name) for name in names]
            df.index = names

        return df
