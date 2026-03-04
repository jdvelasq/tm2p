"""
Network Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.countries  import NodeDegreeDataFrame
    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
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
       Node                    Name  Degree
    0     0         Germany 07:1814      11
    1     1  United Kingdom 03:0636       8
    2     2     Netherlands 03:0300       8
    3     3         Denmark 02:0330       8
    4     4           China 08:1085       7



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
            .unit_of_analysis("countries")
            .run()
        )
