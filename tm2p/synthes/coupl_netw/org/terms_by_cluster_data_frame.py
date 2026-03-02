"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.organizations import TermsByClusterDataFrame
    >>> (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
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
    ... ).head()
                                             0  ...                                                  2
    0       Goethe Univ Frankfurt (DEU) 2:1065  ...  Max Planck Inst for Innovation and Competition...
    1              Univ of Sydney (AUS) 2:0300  ...                     Sungkyunkwan Univ (KOR) 2:0307
    2     Pennsylvania State Univ (USA) 1:0576  ...
    3  Singapore Manag Univ (SMU) (SGP) 1:0576  ...
    4            Univ of Delaware (USA) 1:0576  ...
    <BLANKLINE>
    [5 rows x 3 columns]



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.coupl_netw._intern.from_others.terms_by_cluster_data_frame import (
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
            .update(terms_order_by="OCC")
            .unit_of_analysis("organizations")
            .run()
        )
