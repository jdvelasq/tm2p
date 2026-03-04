"""
Node Degree Dataframe
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.documents  import NodeDegreeDataFrame
    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
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
       Node                                               Name  Degree
    0     0                   Hu Z., 2019, SYMMETRY, V11 1:176       7
    1     1  Gomber P., 2018, J MANAGE INF SYST, V35, P220 ...       4
    2     2       Gomber P., 2017, J BUS ECON, V87, P537 1:489       4
    3     3       Alt R., 2018, ELECTRON MARK, V28, P235 1:150       4
    4     4  Anagnostopoulos I., 2018, J ECON BUS, V100, P7...       2



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.nx import (
    assign_degree_to_nodes,
    collect_node_degrees,
    create_node_degrees_data_frame,
)
from tm2p.synthes.netw.cit._intern.from_documents.create_nx_graph import (
    internal__create_nx_graph,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = assign_degree_to_nodes(nx_graph)
        node_degrees = collect_node_degrees(nx_graph)
        data_frame = create_node_degrees_data_frame(node_degrees)

        return data_frame
