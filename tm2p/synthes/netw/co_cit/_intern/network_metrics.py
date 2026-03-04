"""
Network Metrics
===============================================================================


## >>> from tm2p.packages.co_citation_network import NetworkMetrics
## >>> (
## ...     NetworkMetrics()
## ...     #
## ...     # UNIT OF ANALYSIS:
## ...         unit_of_analysis="cited_sources", # "cited_sources",
## ...                                           # "cited_references",
## ...                                           # "cited_authors"
## ...     .having_items_in_top(30)
## ...     .using_citation_threshold(0)
## ...     .having_items_in(None)
## ...     #
## ...     # DATABASE:
## ...     .where_root_directory("tests/fintech/")
## ...     .where_database("main")
## ...     .where_record_years_range(None, None)
## ...     .where_record_citations_range(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .run()
## ... ).head()
                                Degree  Betweenness  Closeness  PageRank
ELECT COMMER RES APPL 1:32          27     0.077741   0.935484  0.047163
J MANAGE INF SYST 1:27              26     0.017028   0.906250  0.042947
MIS QUART MANAGE INF SYST 1:47      26     0.017028   0.906250  0.042947
COMMUN ACM 1:12                     25     0.070961   0.878788  0.044207
MANAGE SCI 1:30                     25     0.016051   0.878788  0.041488

"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx.compute_network_metrics import compute_network_metrics
from tm2p.synthes.netw.co_cit._intern.create_nx_graph import internal__create_nx_graph


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        nx_graph = internal__create_nx_graph(self.params)
        return compute_network_metrics(params=self.params, nx_graph=nx_graph)

    def run(self):
        nx_graph = internal__create_nx_graph(self.params)
        return compute_network_metrics(params=self.params, nx_graph=nx_graph)
