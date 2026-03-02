"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_references import NetworkMetrics
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
                                               Degree  ...  PageRank
    Leong C., 2017, INT J INF MANAGE 1:2            9  ...  0.112350
    Zavolokina L., 2016, FINANCIAL INNOV 1:3        8  ...  0.104955
    Gabor D., 2017, NEW POLIT ECON 1:2              6  ...  0.073296
    Ryu H.-S., 2018, IND MANAGE DATA SYS 1:2        6  ...  0.073296
    Alt R., 2018, ELECTRON MARK 1:1                 6  ...  0.073296
    Gai K., 2018, J NETWORK COMPUT APPL 1:1         6  ...  0.073296
    Stewart H., 2018, INF COMPUT SECURITY 1:1       6  ...  0.073296
    Gomber P., 2017, J BUS ECON 1:4                 4  ...  0.067991
    Gomber P., 2018, J MANAGE INF SYST 1:3          4  ...  0.061311
    Lee I., 2018, BUS HORIZ 1:2                     4  ...  0.061311
    Chen L., 2016, CHINA ECON J 1:1                 3  ...  0.046669
    Jagtiani J., 2018, J ECON BUS 1:2               1  ...  0.066667
    Anagnostopoulos I., 2018, J ECON BUS 1:1        1  ...  0.066667
    Gozman D., 2018, J MANAGE INF SYST 1:1          1  ...  0.024448
    Li Y., 2017, FINANCIAL INNOV 1:1                1  ...  0.021151
    <BLANKLINE>
    [15 rows x 4 columns]


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
    Leong C., 2017, INT J INF MANAGE            9     0.208791   0.642857  0.112350
    Zavolokina L., 2016, FINANCIAL INNOV        8     0.238095   0.642857  0.104955
    Gabor D., 2017, NEW POLIT ECON              6     0.000000   0.541353  0.073296
    Ryu H.-S., 2018, IND MANAGE DATA SYS        6     0.000000   0.541353  0.073296
    Alt R., 2018, ELECTRON MARK                 6     0.000000   0.541353  0.073296
    Gai K., 2018, J NETWORK COMPUT APPL         6     0.000000   0.541353  0.073296
    Stewart H., 2018, INF COMPUT SECURITY       6     0.000000   0.541353  0.073296
    Gomber P., 2017, J BUS ECON                 4     0.142857   0.514286  0.067991
    Gomber P., 2018, J MANAGE INF SYST          4     0.018315   0.489796  0.061311
    Lee I., 2018, BUS HORIZ                     4     0.018315   0.489796  0.061311
    Chen L., 2016, CHINA ECON J                 3     0.000000   0.447205  0.046669
    Jagtiani J., 2018, J ECON BUS               1     0.000000   0.071429  0.066667
    Anagnostopoulos I., 2018, J ECON BUS        1     0.000000   0.071429  0.066667
    Gozman D., 2018, J MANAGE INF SYST          1     0.000000   0.331797  0.024448
    Li Y., 2017, FINANCIAL INNOV                1     0.000000   0.380952  0.021151




"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.intellect_struct.co_cit_netw._intern.network_metrics import (
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
            .unit_of_analysis("cited_references")
            .run()
        )
