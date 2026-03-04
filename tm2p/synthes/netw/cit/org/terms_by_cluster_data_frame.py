"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.organizations import TermsByClusterDataFrame
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
                                                       0  ...                               3
    0                        Univ of Zurich (CHE) 3:0434  ...  Sungkyunkwan Univ (KOR) 2:0307
    1  Max Planck Inst for Innovation and Competition...  ...   Univ of Zaragoza (ESP) 1:0225
    2                         SKEMA Bus Sch (FRA) 1:0258  ...
    3                        Univ of Bremen (DEU) 1:0258  ...
    4          Univ of Lille Nord de France (FRA) 1:0258  ...
    5  [UKN] CESifo, Poschingerstr. 5, Munich, 81679,...  ...
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
            .unit_of_analysis("organizations")
            .run()
        )
