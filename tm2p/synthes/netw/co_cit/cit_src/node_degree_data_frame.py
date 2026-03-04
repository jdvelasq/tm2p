"""
Node Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_sources import NodeDegreeDataFrame
    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()
       Node                     Name  Degree
    0     0     INT J INF MANAGE 1:2       9
    1     1      FINANCIAL INNOV 1:4       7
    2     2  IND MANAGE DATA SYS 1:2       6
    3     3       NEW POLIT ECON 1:2       6
    4     4        ELECTRON MARK 1:1       6




"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_cit._intern.node_degree_data_frame import (
    NodeDegreeDataFrame as InternalNodeDegreeDataFrame,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalNodeDegreeDataFrame()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_sources")
            .run()
        )
