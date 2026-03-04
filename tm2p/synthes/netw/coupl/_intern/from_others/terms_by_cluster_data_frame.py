"""

## >>> from tm2p.coupling_network._core.others.terms_by_cluster_frame import _terms_by_cluster_frame
## >>> _terms_by_cluster_frame(
## ...     unit_of_analysis='authors', # authors, countries, organizations, sources
## ...     #
## ...     # COLUMN PARAMS:
## ...     top_n=20,
## ...     citations_threshold=0,
## ...     occurrence_threshold=2,
## ...     custom_terms=None,
## ...     #
## ...     # DATABASE:
## ...     .where_root_directory("tests/fintech/")
## ...     .where_database("main")
## ...     .where_record_years_range(None, None)
## ...     .where_record_citations_range(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .run()
## ... )
##                     0                     1                2
## 0    Gomber P. 2:1065      Dolata M. 2:0181    Gai K. 2:0323
## 1    Hornuf L. 2:0358     Schwabe G. 2:0181    Qiu M. 2:0323
## 2  Jagtiani J. 3:0317  Zavolokina L. 2:0181  Sun X./3 2:0323
## 3   Lemieux C. 2:0253



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import cluster_nx_graph, extract_communities_to_frame
from tm2p.synthes.netw.coupl._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class InternalTermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = cluster_nx_graph(self.params, nx_graph)
        return extract_communities_to_frame(self.params, nx_graph)


#
