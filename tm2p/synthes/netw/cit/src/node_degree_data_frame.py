"""
Node Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.sources import NodeDegreeDataFrame
    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
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
       Node                     Name  Degree
    0     0           Symmetry 1:176       7
    1     1  J Manage Inf Syst 2:696       5
    2     2     Sustainability 2:150       5
    3     3      J. Econ. Bus. 3:422       4
    4     4    Electron. Mark. 2:287       4



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.from_others.node_degree_data_frame import (
    NodeDegreeDataFrame as OtherNodeDegreeDataFrame,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            OtherNodeDegreeDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("source_title_abbr")
            .run()
        )
