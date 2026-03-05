from tm2p._intern import ParamsMixin
from tm2p._intern.nx import create_node_degree_plot

from .node_degree_data_frame import NodeDegreeDataFrame


class NodeDegreePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = NodeDegreeDataFrame().update(**self.params.__dict__).run()
        plot = create_node_degree_plot(self.params, df)

        return plot
