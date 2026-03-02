"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.sources import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
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
    Electron. Mark. 2:287           5     0.404762   0.777778  0.231592
    J. Econ. Bus. 3:422             4     0.349206   0.700000  0.177251
    Ind Manage Data Sys 2:386       3     0.063492   0.583333  0.111571
    Symmetry 1:176                  3     0.119048   0.636364  0.110623
    J Manage Inf Syst 2:696         2     0.000000   0.583333  0.135259
    Sustainability 2:150            2     0.015873   0.538462  0.106338
    J. Innov. Manag. 1:226          2     0.000000   0.538462  0.078484
    Financ. Manage. 2:161           1     0.000000   0.437500  0.048882


Smoke tests:
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
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
    Electron. Mark.           5     0.404762   0.777778  0.231592
    J. Econ. Bus.             4     0.349206   0.700000  0.177251
    Ind Manage Data Sys       3     0.063492   0.583333  0.111571
    Symmetry                  3     0.119048   0.636364  0.110623
    J Manage Inf Syst         2     0.000000   0.583333  0.135259
    Sustainability            2     0.015873   0.538462  0.106338
    J. Innov. Manag.          2     0.000000   0.538462  0.078484
    Financ. Manage.           1     0.000000   0.437500  0.048882



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.coupl_netw._intern.from_others.network_metrics import (
    InternalNetworkMetrics,
)


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNetworkMetrics()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("source_title_abbr")
            .run()
        )
