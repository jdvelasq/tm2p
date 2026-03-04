"""
Network Degree Frame
===============================================================================

Smoke tests:
    >>> from tm2p.packages.networks.coupling.sources  import NodeDegreeDataFrame

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

    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
       Node                       Name  Degree
    0     0      Electron. Mark. 2:287       5
    1     1        J. Econ. Bus. 3:422       4
    2     2  Ind Manage Data Sys 2:386       3
    3     3             Symmetry 1:176       3
    4     4    J Manage Inf Syst 2:696       2
    5     5       Sustainability 2:150       2
    6     6     J. Innov. Manag. 1:226       2
    7     7      Financ. Manage. 2:161       1

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
    ... )


    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.from_others.node_degree_data_frame import (
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
            .unit_of_analysis("source_title_abbr")
            .run()
        )
