"""
Terms by Cluster Frame
===============================================================================



Smoke tests:
    >>> from tm2p.packages.networks.co_citation.cited_sources import TermsByClusterDataFrame
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
    ... ).head()
                             0                      1
    0      FINANCIAL INNOV 1:4         J BUS ECON 1:4
    1  IND MANAGE DATA SYS 1:2  J MANAGE INF SYST 1:4
    2       NEW POLIT ECON 1:2          BUS HORIZ 1:2
    3        ELECTRON MARK 1:1   INT J INF MANAGE 1:2
    4  INF COMPUT SECURITY 1:1       CHINA ECON J 1:1



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_cit._intern.terms_by_cluster_data_frame import (
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
            .unit_of_analysis("cited_sources")
            .run()
        )
