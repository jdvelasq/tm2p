"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_sources import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head(15)
                               Degree  Betweenness  Closeness  PageRank
    INT J INF MANAGE 1:2            9     0.377778   0.909091  0.143755
    FINANCIAL INNOV 1:4             7     0.118519   0.769231  0.110731
    IND MANAGE DATA SYS 1:2         6     0.000000   0.714286  0.093828
    NEW POLIT ECON 1:2              6     0.000000   0.714286  0.093828
    ELECTRON MARK 1:1               6     0.000000   0.714286  0.093828
    INF COMPUT SECURITY 1:1         6     0.000000   0.714286  0.093828
    J NETWORK COMPUT APPL 1:1       6     0.000000   0.714286  0.093828
    J MANAGE INF SYST 1:4           4     0.018519   0.625000  0.077923
    BUS HORIZ 1:2                   4     0.018519   0.625000  0.077923
    J BUS ECON 1:4                  3     0.022222   0.588235  0.060200
    CHINA ECON J 1:1                3     0.000000   0.588235  0.060331



    >>> from tm2p.packages.networks.co_citation.cited_sources import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head(15)
                           Degree  Betweenness  Closeness  PageRank
    INT J INF MANAGE            9     0.377778   0.909091  0.143755
    FINANCIAL INNOV             7     0.118519   0.769231  0.110731
    IND MANAGE DATA SYS         6     0.000000   0.714286  0.093828
    NEW POLIT ECON              6     0.000000   0.714286  0.093828
    ELECTRON MARK               6     0.000000   0.714286  0.093828
    INF COMPUT SECURITY         6     0.000000   0.714286  0.093828
    J NETWORK COMPUT APPL       6     0.000000   0.714286  0.093828
    J MANAGE INF SYST           4     0.018519   0.625000  0.077923
    BUS HORIZ                   4     0.018519   0.625000  0.077923
    J BUS ECON                  3     0.022222   0.588235  0.060200
    CHINA ECON J                3     0.000000   0.588235  0.060331




"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_cit._intern.network_metrics import (
    NetworkMetrics as InternalNetworkMetrics,
)


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNetworkMetrics()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_sources")
            .run()
        )
