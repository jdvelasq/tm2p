"""
Network Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.organizations  import NodeDegreeDataFrame

    >>> df = (
    ...     NodeDegreeDataFrame()
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


    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
    Node                                               Name  Degree
    0     0                 Goethe Univ Frankfurt (DEU) 2:1065       4
    1     1                        Univ of Sydney (AUS) 2:0300       4
    2     2               Pennsylvania State Univ (USA) 1:0576       4
    3     3            Singapore Manag Univ (SMU) (SGP) 1:0576       4
    4     4                      Univ of Delaware (USA) 1:0576       4
    5     5       Fed Reserv Bank of Philadelphia (USA) 3:0317       1
    6     6  Max Planck Inst for Innovation and Competition...       1
    7     7                     Sungkyunkwan Univ (KOR) 2:0307       1
    8     8            Fed Reserv Bank of Chicago (USA) 2:0253       1

    >>> df = (
    ...     NodeDegreeDataFrame()
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

    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
       Node                                               Name  Degree
    0     0                 Goethe Univ Frankfurt (DEU) 2:1065       4
    1     1                        Univ of Sydney (AUS) 2:0300       4
    2     2               Pennsylvania State Univ (USA) 1:0576       4
    3     3            Singapore Manag Univ (SMU) (SGP) 1:0576       4
    4     4                      Univ of Delaware (USA) 1:0576       4
    5     5       Fed Reserv Bank of Philadelphia (USA) 3:0317       1
    6     6  Max Planck Inst for Innovation and Competition...       1
    7     7                     Sungkyunkwan Univ (KOR) 2:0307       1
    8     8            Fed Reserv Bank of Chicago (USA) 2:0253       1



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.coupl_netw._intern.from_others.node_degree_data_frame import (
    InternalNodeDegreeDataFrame,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNodeDegreeDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("organizations")
            .run()
        )
