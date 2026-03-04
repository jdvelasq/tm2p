"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.countries import NetworkMetrics
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
    Germany 07:1814             11     0.362374   0.923077  0.207123
    United Kingdom 03:0636       8     0.055556   0.750000  0.114492
    Netherlands 03:0300          8     0.041667   0.750000  0.115797
    Denmark 02:0330              8     0.041667   0.750000  0.108624
    China 08:1085                7     0.188131   0.705882  0.092674
    United States 16:3189        6     0.000000   0.631579  0.073941
    Australia 05:0783            6     0.000000   0.631579  0.061156
    Singapore 01:0576            6     0.000000   0.631579  0.073941
    South Korea 06:1192          4     0.022727   0.600000  0.046426
    Indonesia 01:0102            4     0.000000   0.600000  0.037294
    Switzerland 04:0660          2     0.000000   0.521739  0.032006
    France 01:0258               1     0.000000   0.500000  0.017826
    Spain 01:0225                1     0.000000   0.428571  0.018700



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
    Germany             11     0.362374   0.923077  0.207123
    United Kingdom       8     0.055556   0.750000  0.114492
    Netherlands          8     0.041667   0.750000  0.115797
    Denmark              8     0.041667   0.750000  0.108624
    China                7     0.188131   0.705882  0.092674
    United States        6     0.000000   0.631579  0.073941
    Australia            6     0.000000   0.631579  0.061156
    Singapore            6     0.000000   0.631579  0.073941
    South Korea          4     0.022727   0.600000  0.046426
    Indonesia            4     0.000000   0.600000  0.037294
    Switzerland          2     0.000000   0.521739  0.032006
    France               1     0.000000   0.500000  0.017826
    Spain                1     0.000000   0.428571  0.018700







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
            .unit_of_analysis("countries")
            .update(terms_order_by="OCC")
            .run()
        )
