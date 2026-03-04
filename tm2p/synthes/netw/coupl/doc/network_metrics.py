"""
Network Metrics
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.coupling.documents import NetworkMetrics
    >>> (
    ...     NetworkMetrics()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(20)
    ...     .using_citation_threshold(0)
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
                                                Degree  ...  PageRank
    Anagnostopoulos I., 2018, J ECON BUS 1:202       5  ...  0.091922
    Hu Z., 2019, SYMMETRY 1:176                      5  ...  0.105354
    Alt R., 2018, ELECTRON MARK 1:150                5  ...  0.104977
    Gomber P., 2018, J MANAGE INF SYST 1:576         3  ...  0.055637
    Schueffel P., 2016, J INNOV MANAG 1:226          3  ...  0.062500
    <BLANKLINE>
    [5 rows x 4 columns]



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import compute_network_metrics
from tm2p.synthes.netw.coupl._intern.from_documents.create_nx_graph import (
    internal__create_nx_graph,
)


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(params=self.params)
        return compute_network_metrics(params=self.params, nx_graph=nx_graph)
        nx_graph = internal__create_nx_graph(params=self.params)
        return compute_network_metrics(params=self.params, nx_graph=nx_graph)
