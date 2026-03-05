"""
NetworkMetrics
===============================================================================

Smoke tests:
    >>> from tm2p import CoCitationUnit
    >>> from tm2p.synthes.netw.co_cit import NetworkMetrics
    >>> df = (
    ...     NetworkMetrics()
    ...     #
    ...     # ANALYSIS UNIT:
    ...     .with_co_citation_unit(CoCitationUnit.CITED_REF)
    ...     .having_items_in_top(30)
    ...     .having_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())  # doctest: +NORMALIZE_WHITESPACE
                                                             DEGREE  BETWEENNESS  CLOSENESS  PAGERANK
    Anagnostopoulos, 2018, J ECON BUS 1:10                        7     0.324615   0.377622  0.092316
    Allison, 2015, ENTREPRENEURSHIP THEORY AND PRACTICE 1:4       6     0.246154   0.327935  0.071538
    Arner, 2020, EUR BUS ORGAN LAW REV 1:6                        5     0.200000   0.319527  0.070945
    Ahlers, 2015, ENTREPRENEURSHIP THEORY AND PRACTICE 1:5        4     0.052308   0.244344  0.050385
    Agrawal, 2015, J ECONOMICS AND MANAGEMENT STRATEGY 1:3        3     0.000000   0.239645  0.036833



"""

from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx.compute_network_metrics import compute_network_metrics
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import create_nx_graph


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

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
