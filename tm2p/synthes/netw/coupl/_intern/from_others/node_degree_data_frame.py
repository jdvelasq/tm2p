"""

## >>> from tm2p.coupling_network._core.others.node_degree_frame import _node_degree_frame
## >>> _node_degree_frame(
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
## ... ).head()
   Node                Name  Degree
0     0    Gomber P. 2:1065       3
1     1    Hornuf L. 2:0358       3
2     2  Jagtiani J. 3:0317       3
3     3   Lemieux C. 2:0253       3
4     4    Dolata M. 2:0181       2





"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    internal__assign_degree_to_nodes,
    internal__collect_node_degrees,
    internal__create_node_degrees_data_frame,
)
from tm2p.synthes.netw.coupl._intern.from_others.create_nx_graph import (
    internal__create_nx_graph,
)


class InternalNodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(params=self.params)
        nx_graph = internal__assign_degree_to_nodes(nx_graph)
        node_degrees = internal__collect_node_degrees(nx_graph)
        data_frame = internal__create_node_degrees_data_frame(node_degrees)

        return data_frame
        node_degrees = internal__collect_node_degrees(nx_graph)
        data_frame = internal__create_node_degrees_data_frame(node_degrees)

        return data_frame
