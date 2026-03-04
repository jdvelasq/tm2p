"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.organizations import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
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
                                                        Degree  ...  PageRank
    Goethe Univ Frankfurt (DEU) 2:1065                       4  ...  0.120134
    Univ of Sydney (AUS) 2:0300                              4  ...  0.075018
    Pennsylvania State Univ (USA) 1:0576                     4  ...  0.120134
    Singapore Manag Univ (SMU) (SGP) 1:0576                  4  ...  0.120134
    Univ of Delaware (USA) 1:0576                            4  ...  0.120134
    Fed Reserv Bank of Philadelphia (USA) 3:0317             1  ...  0.111111
    Max Planck Inst for Innovation and Competition ...       1  ...  0.111111
    Sungkyunkwan Univ (KOR) 2:0307                           1  ...  0.111111
    Fed Reserv Bank of Chicago (USA) 2:0253                  1  ...  0.111111
    <BLANKLINE>
    [9 rows x 4 columns]



    >>> from tm2p.packages.networks.coupling.organizations import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
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
                                                        Degree  ...  PageRank
    Goethe Univ Frankfurt (DEU)                              4  ...  0.120134
    Univ of Sydney (AUS)                                     4  ...  0.075018
    Pennsylvania State Univ (USA)                            4  ...  0.120134
    Singapore Manag Univ (SMU) (SGP)                         4  ...  0.120134
    Univ of Delaware (USA)                                   4  ...  0.120134
    Fed Reserv Bank of Philadelphia (USA)                    1  ...  0.111111
    Max Planck Inst for Innovation and Competition ...       1  ...  0.111111
    Sungkyunkwan Univ (KOR)                                  1  ...  0.111111
    Fed Reserv Bank of Chicago (USA)                         1  ...  0.111111
    <BLANKLINE>
    [9 rows x 4 columns]





"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.from_others.network_metrics import (
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
            .unit_of_analysis("organizations")
            .run()
        )
