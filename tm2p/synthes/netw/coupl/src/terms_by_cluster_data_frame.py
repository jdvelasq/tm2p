"""
Terms by Cluster Frame
===============================================================================

Smoke tests:
    >>> from tm2p.packages.networks.coupling.sources import TermsByClusterDataFrame

    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_ordered_by("OCC")
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


    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
                               0                        1
    0  Ind Manage Data Sys 2:386      J. Econ. Bus. 3:422
    1      Electron. Mark. 2:287  J Manage Inf Syst 2:696
    2       Sustainability 2:150    Financ. Manage. 2:161
    3     J. Innov. Manag. 1:226
    4             Symmetry 1:176


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.from_others.terms_by_cluster_data_frame import (
    InternalTermsByClusterDataFrame,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            InternalTermsByClusterDataFrame()
            .update(**self.params.__dict__)
            .unit_of_analysis("source_title_abbr")
            .run()
        )
