"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.documents import TermsByClusterDataFrame
    >>> (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .using_item_counters(True)
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
                                                       0  ...                                                  3
    0    Gabor D., 2017, NEW POLIT ECON, V22, P423 1:314  ...  Anagnostopoulos I., 2018, J ECON BUS, V100, P7...
    1  Gai K., 2018, J NETWORK COMPUT APPL, V103, P26...  ...     Zavolokina L., 2016, FINANCIAL INNOV, V2 1:106
    2  Belanche D., 2019, IND MANAGE DATA SYS, V119, ...  ...
    3   Leong C., 2017, INT J INF MANAGE, V37, P92 1:180  ...
    4                   Hu Z., 2019, SYMMETRY, V11 1:176  ...
    <BLANKLINE>
    [5 rows x 4 columns]



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import cluster_nx_graph, extract_communities_to_frame
from tm2p.synthes.netw.cit._intern.from_documents.create_nx_graph import (
    internal__create_nx_graph,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        return extract_communities_to_frame(self.params, nx_graph)
