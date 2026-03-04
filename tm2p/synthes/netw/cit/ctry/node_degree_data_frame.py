"""
Node Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.countries  import NodeDegreeDataFrame
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
       Node                   Name  Degree
    0     0        Germany 07:1814      13
    1     1          China 08:1085      12
    2     2  United States 16:3189       9
    3     3      Singapore 01:0576       8
    4     4    South Korea 06:1192       7


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
            .unit_of_analysis("countries")
            .run()
        )
