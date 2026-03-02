"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_references import TermsByClusterDataFrame
    >>> (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_items_in(None)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head(10)
                                               0  ...                                         2
    0   Zavolokina L., 2016, FINANCIAL INNOV 1:3  ...         Jagtiani J., 2018, J ECON BUS 1:2
    1         Gabor D., 2017, NEW POLIT ECON 1:2  ...  Anagnostopoulos I., 2018, J ECON BUS 1:1
    2   Ryu H.-S., 2018, IND MANAGE DATA SYS 1:2  ...
    3            Alt R., 2018, ELECTRON MARK 1:1  ...
    4    Gai K., 2018, J NETWORK COMPUT APPL 1:1  ...
    5           Li Y., 2017, FINANCIAL INNOV 1:1  ...
    6  Stewart H., 2018, INF COMPUT SECURITY 1:1  ...
    <BLANKLINE>
    [7 rows x 3 columns]




"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.intellect_struct.co_cit_netw._intern.terms_by_cluster_data_frame import (
    TermsByClusterDataFrame as InternalTermsByClusterDataFrame,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalTermsByClusterDataFrame()
            .update(**self.params.__dict__)
            .unit_of_analysis("cited_references")
            .run()
        )
