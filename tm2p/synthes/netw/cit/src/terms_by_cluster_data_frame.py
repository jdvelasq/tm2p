"""
Terms by Cluster Frame
===============================================================================

Smoke tests:
    >>> from tm2p.packages.networks.citation.sources import TermsByClusterDataFrame
    >>> (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
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
                                  0  ...                       3
    0          Sustainability 2:150  ...     J. Econ. Bus. 3:422
    1             Bus. Horiz. 1:557  ...  Financial Innov. 2:190
    2        Small Bus. Econ. 1:258  ...   Financ. Manage. 2:161
    3  Busin. Info. Sys. Eng. 1:253  ...
    4        Int J Inf Manage 1:180  ...
    5          China Econ. J. 1:096  ...
    <BLANKLINE>
    [6 rows x 4 columns]


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.from_others.terms_by_cluster_data_frame import (
    TermsByClusterDataFrame as OtherTermsByClusterDataFrame,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            OtherTermsByClusterDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("source_title_abbr")
            .run()
        )
