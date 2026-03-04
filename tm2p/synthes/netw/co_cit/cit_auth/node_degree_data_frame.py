"""
Node Degree Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_authors import NodeDegreeDataFrame
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
       Node               Name  Degree
    0     0       Leong C. 1:2       9
    1     1  Zavolokina L. 1:3       8
    2     2       Gabor D. 1:2       6
    3     3      Ryu H.-S. 1:2       6
    4     4         Alt R. 1:1       6




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
            .unit_of_analysis("cited_authors")
            .run()
        )
