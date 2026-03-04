"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.documents import TermsByClusterDataFrame
    >>> (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
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
    ... )
                                                0  ...                                       3
    0    Gomber P., 2018, J MANAGE INF SYST 1:576  ...  Jagtiani J., 2019, FINANC MANAGE 1:097
    1  Anagnostopoulos I., 2018, J ECON BUS 1:202  ...     Jagtiani J., 2018, J ECON BUS 1:064
    2           Alt R., 2018, ELECTRON MARK 1:150  ...
    3    Gozman D., 2018, J MANAGE INF SYST 1:120  ...
    4  Iman N., 2018, ELECT COMMER RES APPL 1:102  ...
    5         Zhao Q., 2019, SUSTAINABILITY 1:079  ...
    <BLANKLINE>
    [6 rows x 4 columns]


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import cluster_nx_graph, extract_communities
from tm2p.synthes.netw.coupl._intern.from_documents.create_nx_graph import (
    internal__create_nx_graph,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(params=self.params, nx_graph=nx_graph)
        return extract_communities(params=self.params, nx_graph=nx_graph)
