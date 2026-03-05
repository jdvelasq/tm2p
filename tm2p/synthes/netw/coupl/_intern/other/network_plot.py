from tm2p._intern import ParamsMixin, remove_counters
from tm2p._intern.nx import (
    assign_constant_to_edge_colors,
    assign_edge_widths_based_on_weight,
    assign_node_colors_based_on_group_attribute,
    assign_node_sizes_based_on_occurrences,
    assign_text_positions_based_on_quadrants,
    assign_textfont_opacity_based_on_occurrences,
    assign_textfont_sizes_based_on_occurrences,
    cluster_nx_graph,
    compute_spring_layout_positions,
    plot_nx_graph,
)
from tm2p.synthes.netw.coupl._intern.other.create_nx_graph import create_nx_graph


class NetworkPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        use_counters = self.params.counters
        self.params.counters = True

        nx_graph = create_nx_graph(params=self.params)

        nx_graph = cluster_nx_graph(params=self.params, nx_graph=nx_graph)
        nx_graph = compute_spring_layout_positions(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = assign_node_colors_based_on_group_attribute(nx_graph)
        nx_graph = assign_node_sizes_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = assign_textfont_sizes_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = assign_textfont_opacity_based_on_occurrences(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = assign_edge_widths_based_on_weight(
            params=self.params, nx_graph=nx_graph
        )
        nx_graph = assign_text_positions_based_on_quadrants(nx_graph)
        nx_graph = assign_constant_to_edge_colors(params=self.params, nx_graph=nx_graph)

        if use_counters is False:
            self.params.counters = False
            for node, data in nx_graph.nodes(data=True):
                text = data["text"]
                nx_graph.nodes[node]["text"] = remove_counters(text)

        return plot_nx_graph(params=self.params, nx_graph=nx_graph)
