"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_authors import NetworkMetrics
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
    Leong C. 1:2                 9     0.217949   0.715976  0.121107
    Zavolokina L. 1:3            8     0.192308   0.664835  0.111071
    Gabor D. 1:2                 6     0.000000   0.547511  0.078353
    Ryu H.-S. 1:2                6     0.000000   0.547511  0.078353
    Alt R. 1:1                   6     0.000000   0.547511  0.078353
    Gai K. 1:1                   6     0.000000   0.547511  0.078353
    Stewart H. 1:1               6     0.000000   0.547511  0.078353
    Gomber P. 1:7                5     0.153846   0.547511  0.084011
    Lee I. 1:2                   3     0.000000   0.465385  0.050839
    Chen L. 1:1                  3     0.000000   0.465385  0.050839
    Jagtiani J. 1:2              1     0.000000   0.076923  0.071429
    Anagnostopoulos I. 1:1       1     0.000000   0.076923  0.071429
    Gozman D. 1:1                1     0.000000   0.344729  0.024996
    Li Y. 1:1                    1     0.000000   0.387821  0.022516



    >>> from tm2p.packages.networks.co_citation.cited_authors import NetworkMetrics
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
    Leong C.                 9     0.217949   0.715976  0.121107
    Zavolokina L.            8     0.192308   0.664835  0.111071
    Gabor D.                 6     0.000000   0.547511  0.078353
    Ryu H.-S.                6     0.000000   0.547511  0.078353
    Alt R.                   6     0.000000   0.547511  0.078353
    Gai K.                   6     0.000000   0.547511  0.078353
    Stewart H.               6     0.000000   0.547511  0.078353
    Gomber P.                5     0.153846   0.547511  0.084011
    Lee I.                   3     0.000000   0.465385  0.050839
    Chen L.                  3     0.000000   0.465385  0.050839
    Jagtiani J.              1     0.000000   0.076923  0.071429
    Anagnostopoulos I.       1     0.000000   0.076923  0.071429
    Gozman D.                1     0.000000   0.344729  0.024996
    Li Y.                    1     0.000000   0.387821  0.022516





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
            .unit_of_analysis("cited_authors")
            .run()
        )
