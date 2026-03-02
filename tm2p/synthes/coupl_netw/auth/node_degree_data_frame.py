"""
Network Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.authors  import NodeDegreeDataFrame
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
       Node                  Name  Degree
    0     0      Gomber P. 2:1065       3
    1     1  Kauffman R.J. 1:0576       3
    2     2      Parker C. 1:0576       3
    3     3     Weber B.W. 1:0576       3
    4     4    Jagtiani J. 3:0317       1




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
            .unit_of_analysis("authors")
            .run()
        )
