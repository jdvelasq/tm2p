"""
Node Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.organizations  import NodeDegreeDataFrame
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
       Node                                          Name  Degree
    0     0                   Univ of Zurich (CHE) 3:0434       5
    1     1            Goethe Univ Frankfurt (DEU) 2:1065       5
    2     2                   Univ of Sydney (AUS) 2:0300       4
    3     3  Fed Reserv Bank of Philadelphia (USA) 3:0317       2
    4     4       Fed Reserv Bank of Chicago (USA) 2:0253       2



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
            .unit_of_analysis("organizations")
            .run()
        )
